"""Rank portfolios and cost-aware backtests for cross-sectional signals."""

from __future__ import annotations

import pandas as pd


def rank_portfolio(
    signal_frame: pd.DataFrame,
    n_quantiles: int = 5,
    long_short: bool = True,
) -> pd.DataFrame:
    """Convert daily cross-sectional signals into equal-weight positions."""
    required = {"date", "asset", "signal"}
    missing = required.difference(signal_frame.columns)
    if missing:
        raise ValueError(f"signal frame is missing columns: {sorted(missing)}")
    if n_quantiles < 2:
        raise ValueError("n_quantiles must be at least 2")

    frame = signal_frame[["date", "asset", "signal"]].copy()
    frame["date"] = pd.to_datetime(frame["date"])
    output: list[pd.DataFrame] = []
    for date, group in frame.groupby("date", sort=True):
        clean = group.dropna(subset=["signal"]).copy()
        clean["weight"] = 0.0
        if len(clean) >= 2:
            ordered = clean.sort_values(["signal", "asset"], kind="mergesort")
            n_select = max(1, len(ordered) // n_quantiles)
            short_assets = ordered.head(n_select).index
            long_assets = ordered.tail(n_select).index
            clean.loc[long_assets, "weight"] = 1.0 / n_select
            if long_short:
                clean.loc[short_assets, "weight"] = -1.0 / n_select
            else:
                clean.loc[short_assets, "weight"] = 0.0
        output.append(clean)

    if not output:
        return frame.assign(weight=pd.Series(dtype=float))
    return pd.concat(output, ignore_index=True)[["date", "asset", "signal", "weight"]]


def backtest(
    signal_frame: pd.DataFrame,
    returns: pd.DataFrame,
    cost_bps: float = 5.0,
) -> pd.DataFrame:
    """Backtest target weights with turnover-based transaction costs."""
    if cost_bps < 0:
        raise ValueError("cost_bps cannot be negative")
    required_returns = {"date", "asset", "asset_return"}
    missing = required_returns.difference(returns.columns)
    if missing:
        raise ValueError(f"returns frame is missing columns: {sorted(missing)}")

    weights = signal_frame[["date", "asset", "weight"]].copy()
    asset_returns = returns[["date", "asset", "asset_return"]].copy()
    weights["date"] = pd.to_datetime(weights["date"])
    asset_returns["date"] = pd.to_datetime(asset_returns["date"])
    merged = weights.merge(asset_returns, on=["date", "asset"], how="left", validate="one_to_one")
    if merged["asset_return"].isna().any():
        raise ValueError("returns are missing for one or more held assets")

    gross = merged.assign(contribution=merged["weight"] * merged["asset_return"])
    gross_by_date = gross.groupby("date", sort=True)["contribution"].sum().rename("gross_return")
    weight_matrix = weights.pivot(index="date", columns="asset", values="weight").fillna(0.0).sort_index()
    turnover = weight_matrix.diff().abs().sum(axis=1)
    if len(weight_matrix):
        turnover.iloc[0] = weight_matrix.iloc[0].abs().sum()

    result = pd.concat([gross_by_date, turnover.rename("turnover")], axis=1).fillna(0.0)
    result["cost"] = result["turnover"] * float(cost_bps) / 10_000.0
    result["net_return"] = result["gross_return"] - result["cost"]
    result["wealth"] = (1.0 + result["net_return"]).cumprod()
    return result.reset_index()
