"""Time-ordered validation helpers for financial research."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


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


def walk_forward_model_signal(
    frame: pd.DataFrame,
    feature_columns: Sequence[str],
    model_type: str = "ridge",
    train_size: int = 252,
    test_size: int = 21,
    step: int = 21,
) -> pd.DataFrame:
    """Generate strictly out-of-sample predictions with walk-forward fitting."""
    required = {"date", "asset", "forward_return", *feature_columns}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"model frame is missing columns: {sorted(missing)}")
    if model_type == "ridge":
        model_factory = lambda: make_pipeline(StandardScaler(), Ridge(alpha=1.0))
    elif model_type == "tree":
        model_factory = lambda: HistGradientBoostingRegressor(
            max_iter=120, learning_rate=0.05, max_leaf_nodes=15, random_state=7
        )
    else:
        raise ValueError("model_type must be 'ridge' or 'tree'")

    clean = frame.copy()
    clean["date"] = pd.to_datetime(clean["date"])
    predictions: list[pd.DataFrame] = []
    for train_dates, test_dates in walk_forward_splits(clean["date"], train_size, test_size, step):
        train = clean[clean["date"].isin(train_dates)].dropna(subset=[*feature_columns, "forward_return"])
        test = clean[clean["date"].isin(test_dates)].dropna(subset=feature_columns)
        if len(train) < 3 or test.empty:
            continue
        model = model_factory()
        model.fit(train[list(feature_columns)], train["forward_return"])
        predictions.append(
            test[["date", "asset"]].assign(signal=model.predict(test[list(feature_columns)]))
        )

    if not predictions:
        return pd.DataFrame(columns=["date", "asset", "signal"])
    return pd.concat(predictions, ignore_index=True)[["date", "asset", "signal"]]
