"""Time-ordered validation helpers for financial research."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

import pandas as pd


def walk_forward_splits(
    dates: Sequence,
    train_size: int,
    test_size: int,
    step: int,
) -> Iterator[tuple[pd.DatetimeIndex, pd.DatetimeIndex]]:
    """Yield expanding-free, chronological train/test date windows."""
    if min(train_size, test_size, step) < 1:
        raise ValueError("train_size, test_size, and step must be positive")

    unique_dates = pd.DatetimeIndex(sorted(pd.unique(pd.to_datetime(dates))))
    for start in range(0, len(unique_dates) - train_size - test_size + 1, step):
        train_end = start + train_size
        test_end = train_end + test_size
        yield unique_dates[start:train_end], unique_dates[train_end:test_end]
