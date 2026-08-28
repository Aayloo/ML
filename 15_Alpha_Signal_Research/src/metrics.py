"""Predictive and portfolio performance metrics."""

from __future__ import annotations

import numpy as np
import pandas as pd


def cross_sectional_ic(
    frame: pd.DataFrame,
    signal_col: str = "signal",
    target_col: str = "forward_return",
) -> pd.Series:
    """Calculate daily Spearman information coefficient by cross-section."""
    values: list[float] = []
    dates: list[pd.Timestamp] = []
    for date, group in frame.groupby("date", sort=True):
        clean = group[[signal_col, target_col]].dropna()
        if len(clean) < 3 or clean[signal_col].nunique() < 2 or clean[target_col].nunique() < 2:
            continue
        values.append(clean[signal_col].corr(clean[target_col], method="spearman"))
        dates.append(pd.Timestamp(date))
    return pd.Series(values, index=pd.DatetimeIndex(dates), name="ic", dtype=float)


def performance_summary(returns: pd.Series, periods_per_year: int = 252) -> dict[str, float]:
    """Return annualized return, volatility, Sharpe, and maximum drawdown."""
    clean = pd.Series(returns, dtype=float).dropna()
    if clean.empty:
        return {
            "annualized_return": 0.0,
            "annualized_volatility": 0.0,
            "sharpe": 0.0,
            "max_drawdown": 0.0,
        }

    wealth = (1.0 + clean).cumprod()
    years = len(clean) / periods_per_year
    annualized_return = float(wealth.iloc[-1] ** (1.0 / years) - 1.0) if wealth.iloc[-1] > 0 else -1.0
    annualized_volatility = float(clean.std(ddof=1) * np.sqrt(periods_per_year)) if len(clean) > 1 else 0.0
    sharpe = float(clean.mean() / clean.std(ddof=1) * np.sqrt(periods_per_year)) if len(clean) > 1 and clean.std(ddof=1) > 0 else 0.0
    drawdown = wealth / wealth.cummax() - 1.0
    return {
        "annualized_return": annualized_return,
        "annualized_volatility": annualized_volatility,
        "sharpe": sharpe,
        "max_drawdown": float(drawdown.min()),
    }


def quantile_spread(
    frame: pd.DataFrame,
    n_quantiles: int = 5,
    signal_col: str = "signal",
    target_col: str = "forward_return",
) -> pd.Series:
    """Return top-quantile minus bottom-quantile forward returns by date."""
    if n_quantiles < 2:
        raise ValueError("n_quantiles must be at least 2")
    spreads: list[float] = []
    dates: list[pd.Timestamp] = []
    for date, group in frame.groupby("date", sort=True):
        clean = group[[signal_col, target_col]].dropna().sort_values(signal_col)
        if len(clean) < n_quantiles:
            continue
        buckets = np.minimum(
            (np.arange(len(clean)) * n_quantiles // len(clean)), n_quantiles - 1
        )
        clean = clean.assign(_bucket=buckets)
        bucket_returns = clean.groupby("_bucket")[target_col].mean()
        spreads.append(float(bucket_returns.iloc[-1] - bucket_returns.iloc[0]))
        dates.append(pd.Timestamp(date))
    return pd.Series(spreads, index=pd.DatetimeIndex(dates), name="quantile_spread", dtype=float)
