import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.data import make_demo_market_data
from src.features import build_features
from src.signals import build_signal


def test_forward_return_is_not_available_as_a_feature():
    features = build_features(make_demo_market_data(80, 4), {"horizon": 5})

    feature_columns = {column for column in features.columns if column.endswith("_feature")}
    assert "forward_return" in features.columns
    assert "forward_return" not in feature_columns


def test_all_signal_names_return_the_same_contract():
    features = build_features(make_demo_market_data(80, 4), {"horizon": 5})

    for name in ("momentum", "reversal", "volatility", "liquidity"):
        result = build_signal(features, name, {})
        assert list(result.columns) == ["date", "asset", "signal"]
        assert result["signal"].notna().any()
