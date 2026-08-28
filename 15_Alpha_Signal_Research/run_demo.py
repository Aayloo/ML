"""Run the complete offline Alpha Signal Research workflow."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.data import make_demo_market_data
from src.features import build_features
from src.metrics import cross_sectional_ic, performance_summary, quantile_spread
from src.portfolio import backtest, rank_portfolio
from src.reporting import save_report
from src.signals import build_signal
from src.validation import walk_forward_model_signal


def run_demo(output_dir: str | Path = "reports/demo", signal_name: str = "momentum") -> dict:
    """Run factor and walk-forward ML experiments without network access."""
    market_data = make_demo_market_data(n_days=720, n_assets=24, seed=7)
    features = build_features(
        market_data,
        {
            "horizon": 5,
            "momentum_lookback": 21,
            "reversal_lookback": 5,
            "volatility_lookback": 21,
            "liquidity_lookback": 21,
        },
    )
    returns = features[["date", "asset"]].copy()
    returns["asset_return"] = features.groupby("asset", sort=False)["close"].pct_change()

    factor_signal = build_signal(features, signal_name)
    factor_frame = factor_signal.merge(
        features[["date", "asset", "forward_return"]], on=["date", "asset"], how="left", validate="one_to_one"
    )
    factor_weights = rank_portfolio(factor_signal, n_quantiles=5, long_short=True)
    factor_daily = backtest(factor_weights, returns, cost_bps=5.0)

    model_features = [
        "momentum_feature",
        "reversal_feature",
        "volatility_feature",
        "liquidity_feature",
    ]
    model_signal = walk_forward_model_signal(
        features,
        model_features,
        model_type="ridge",
        train_size=252,
        test_size=21,
        step=21,
    )
    model_frame = model_signal.merge(
        features[["date", "asset", "forward_return"]], on=["date", "asset"], how="left", validate="one_to_one"
    )
    model_weights = rank_portfolio(model_signal, n_quantiles=5, long_short=True)
    model_daily = backtest(model_weights, returns, cost_bps=5.0)

    results = {
        "signal_name": signal_name,
        "factor_daily": factor_daily,
        "model_daily": model_daily,
        "factor_ic": cross_sectional_ic(factor_frame),
        "model_ic": cross_sectional_ic(model_frame),
        "factor_spread": quantile_spread(factor_frame),
        "model_spread": quantile_spread(model_frame),
        "factor_summary": performance_summary(factor_daily["net_return"]),
        "model_summary": performance_summary(model_daily["net_return"]),
    }
    return save_report(results, output_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the offline Alpha Signal Research demo")
    parser.add_argument("--signal", default="momentum", choices=["momentum", "reversal", "volatility", "liquidity"])
    parser.add_argument("--output-dir", default="reports/demo")
    args = parser.parse_args()
    summary = run_demo(output_dir=args.output_dir, signal_name=args.signal)
    print(f"Generated report in {Path(args.output_dir)}")
    for key, value in summary.items():
        print(f"{key}: {value:.4f}")


if __name__ == "__main__":
    main()
