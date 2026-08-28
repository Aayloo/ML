import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.portfolio import backtest, rank_portfolio


def sample_signals() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": ["2020-01-01"] * 6 + ["2020-01-02"] * 6,
            "asset": list("ABCDEF") * 2,
            "signal": [1, 2, 3, 4, 5, 6, 6, 5, 4, 3, 2, 1],
        }
    )


def sample_returns() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": ["2020-01-01"] * 6 + ["2020-01-02"] * 6,
            "asset": list("ABCDEF") * 2,
            "asset_return": [0.01, 0.01, 0.0, -0.01, -0.01, -0.01] * 2,
        }
    )


def test_long_short_portfolio_is_cross_sectionally_neutral():
    weights = rank_portfolio(sample_signals(), n_quantiles=3, long_short=True)
    daily = weights.groupby("date")["weight"].sum()

    assert (daily.abs() < 1e-9).all()


def test_transaction_costs_reduce_net_returns():
    weights = rank_portfolio(sample_signals(), n_quantiles=3, long_short=True)
    result = backtest(weights, sample_returns(), cost_bps=10)

    assert (result["net_return"] <= result["gross_return"]).all()
    assert (result["turnover"] >= 0).all()
