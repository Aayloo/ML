"""Feature construction with explicit lagging and cross-sectional hygiene."""

from __future__ import annotations

import numpy as np
import pandas as pd


def _winsorize(series: pd.Series, limit: float = 0.02) -> pd.Series:
    low, high = series.quantile([limit, 1.0 - limit])
    return series.clip(lower=low, upper=high)


def build_features(market_data: pd.DataFrame, config: dict | None = None) -> pd.DataFrame:
    """Build lagged features and a forward-return label from long market data."""
    config = config or {}
    horizon = int(config.get("horizon", 5))
    momentum_lookback = int(config.get("momentum_lookback", 21))
    reversal_lookback = int(config.get("reversal_lookback", 5))
    volatility_lookback = int(config.get("volatility_lookback", 21))
    liquidity_lookback = int(config.get("liquidity_lookback", 21))

    required = {"date", "asset", "close", "volume"}
    missing = required.difference(market_data.columns)
    if missing:
        raise ValueError(f"market data is missing columns: {sorted(missing)}")
    if horizon < 1:
        raise ValueError("horizon must be positive")

    frame = market_data.sort_values(["asset", "date"]).copy()
    grouped_close = frame.groupby("asset", sort=False)["close"]
    grouped_volume = frame.groupby("asset", sort=False)["volume"]
    daily_return = grouped_close.pct_change()

    raw_features = pd.DataFrame(index=frame.index)
    raw_features["momentum_feature"] = grouped_close.pct_change(momentum_lookback)
    raw_features["reversal_feature"] = -grouped_close.pct_change(reversal_lookback)
    raw_features["volatility_feature"] = -daily_return.groupby(frame["asset"]).transform(
        lambda values: values.rolling(volatility_lookback, min_periods=volatility_lookback).std()
    )
    dollar_volume = frame["close"] * frame["volume"]
    illiquidity = daily_return.abs().div(dollar_volume.replace(0, np.nan)) * 1_000_000
    raw_features["liquidity_feature"] = -illiquidity.groupby(frame["asset"]).transform(
        lambda values: values.rolling(liquidity_lookback, min_periods=liquidity_lookback).mean()
    )

    # Use information available before the portfolio formation date.
    for column in raw_features:
        raw_features[column] = raw_features.groupby(frame["asset"], sort=False)[column].shift(1)
        raw_features[column] = raw_features.groupby(frame["date"], sort=False)[column].transform(_winsorize)

    forward_return = grouped_close.shift(-horizon).div(frame["close"]) - 1.0
    frame = frame[["date", "asset", "close", "volume"]].copy()
    frame["forward_return"] = forward_return
    return pd.concat([frame, raw_features], axis=1).sort_values(["date", "asset"]).reset_index(drop=True)
