import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.data import make_demo_market_data


def test_demo_market_data_is_deterministic_and_wide_enough():
    first = make_demo_market_data(n_days=40, n_assets=4, seed=7)
    second = make_demo_market_data(n_days=40, n_assets=4, seed=7)

    assert first.equals(second)
    assert set(first.columns) == {"date", "asset", "close", "volume"}
    assert first["asset"].nunique() == 4
    assert first["date"].nunique() == 40


def test_demo_market_data_has_positive_prices_and_volume():
    data = make_demo_market_data(n_days=20, n_assets=3)

    assert (data["close"] > 0).all()
    assert (data["volume"] > 0).all()
