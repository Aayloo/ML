"""Deterministic offline data used by the research notebooks and tests."""

from __future__ import annotations

import numpy as np
import pandas as pd


def make_demo_market_data(
    n_days: int = 520,
    n_assets: int = 24,
    seed: int = 7,
) -> pd.DataFrame:
    """Create a small market-like panel with persistent returns.

    The fixture is intentionally synthetic: it makes the project runnable
    without credentials or network access and should never be interpreted as
    evidence of live-market performance.
    """
    if n_days < 2 or n_assets < 2:
        raise ValueError("n_days and n_assets must both be at least 2")

    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2020-01-02", periods=n_days)
    assets = [f"ASSET_{i:02d}" for i in range(n_assets)]
    market_returns = rng.normal(0.00015, 0.008, size=n_days)
    loadings = rng.uniform(0.6, 1.4, size=n_assets)
    asset_drifts = rng.normal(0.00012, 0.00005, size=n_assets)

    rows: list[dict[str, object]] = []
    for asset_idx, asset in enumerate(assets):
        idio = rng.normal(0.0, 0.009, size=n_days)
        returns = np.empty(n_days)
        returns[0] = asset_drifts[asset_idx] + loadings[asset_idx] * market_returns[0] + idio[0]
        for day in range(1, n_days):
            returns[day] = (
                asset_drifts[asset_idx]
                + loadings[asset_idx] * market_returns[day]
                + 0.18 * returns[day - 1]
                + idio[day]
            )
        prices = 100.0 * np.exp(np.cumsum(returns))
        volume = np.exp(rng.normal(np.log(1_000_000), 0.35, size=n_days))
        rows.extend(
            {
                "date": date,
                "asset": asset,
                "close": float(price),
                "volume": float(vol),
            }
            for date, price, vol in zip(dates, prices, volume)
        )

    return (
        pd.DataFrame(rows)
        .sort_values(["date", "asset"])
        .reset_index(drop=True)
    )
