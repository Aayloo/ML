"""Pluggable Alpha signal registry."""

from __future__ import annotations

import pandas as pd


SIGNAL_FEATURES = {
    "momentum": "momentum_feature",
    "reversal": "reversal_feature",
    "volatility": "volatility_feature",
    "liquidity": "liquidity_feature",
}


def build_signal(feature_data: pd.DataFrame, name: str, config: dict | None = None) -> pd.DataFrame:
    """Return a stable date/asset/signal contract for one registered signal."""
    del config
    if name not in SIGNAL_FEATURES:
        available = ", ".join(sorted(SIGNAL_FEATURES))
        raise ValueError(f"unknown signal '{name}'. Available signals: {available}")

    column = SIGNAL_FEATURES[name]
    if column not in feature_data.columns:
        raise ValueError(f"feature data is missing '{column}'")

    result = feature_data[["date", "asset", column]].rename(columns={column: "signal"}).copy()
    result["signal"] = result.groupby("date", sort=False)["signal"].transform(
        lambda values: values.rank(pct=True, method="average") - 0.5
    )
    return result[["date", "asset", "signal"]]
