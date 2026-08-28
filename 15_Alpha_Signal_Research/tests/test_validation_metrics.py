import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.metrics import cross_sectional_ic, performance_summary
from src.validation import walk_forward_splits


def test_walk_forward_splits_never_train_on_future_dates():
    dates = pd.date_range("2020-01-01", periods=10, freq="D")

    splits = list(walk_forward_splits(dates, train_size=5, test_size=2, step=2))

    assert splits
    for train_dates, test_dates in splits:
        assert max(train_dates) < min(test_dates)


def test_cross_sectional_ic_detects_positive_rank_relationship():
    frame = pd.DataFrame(
        {
            "date": ["2020-01-01"] * 4,
            "signal": [1.0, 2.0, 3.0, 4.0],
            "forward_return": [0.01, 0.02, 0.03, 0.04],
        }
    )

    result = cross_sectional_ic(frame)

    assert result.iloc[0] > 0.99


def test_performance_summary_reports_drawdown_and_sharpe_keys():
    summary = performance_summary(pd.Series([0.01, -0.02, 0.01]))

    assert {"annualized_return", "annualized_volatility", "sharpe", "max_drawdown"} <= summary.keys()
