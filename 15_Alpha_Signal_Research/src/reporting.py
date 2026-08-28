"""GitHub-friendly visual reporting for Alpha experiments."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def _write_summary(summary: dict, path: Path, signal_name: str) -> None:
    lines = [
        "# Alpha Signal Research — Offline Demo",
        "",
        f"**Primary signal:** `{signal_name}`",
        "",
        "This report is generated from deterministic synthetic data for pipeline validation. It is not evidence of live-market performance.",
        "",
        "## Performance summary",
        "",
        "| Model | Annualized return | Volatility | Sharpe | Max drawdown |",
        "|---|---:|---:|---:|---:|",
    ]
    for label, metrics in summary.items():
        if not isinstance(metrics, dict):
            continue
        lines.append(
            f"| {label} | {metrics['annualized_return']:.2%} | {metrics['annualized_volatility']:.2%} | "
            f"{metrics['sharpe']:.2f} | {metrics['max_drawdown']:.2%} |"
        )
    lines += [
        "",
        "## Research caveats",
        "",
        "- Replace the demo loader with licensed point-in-time data before drawing investment conclusions.",
        "- Keep the final test period untouched during feature and model selection.",
        "- Re-estimate costs, liquidity, universe membership, and risk controls for any real deployment.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def save_report(results: dict, output_dir: str | Path) -> dict:
    """Save stable PNG/JSON/Markdown artifacts and return summary metrics."""
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    factor_daily = results["factor_daily"]
    model_daily = results.get("model_daily")

    fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
    axes[0].plot(factor_daily["date"], factor_daily["wealth"], label="factor baseline", linewidth=1.8)
    if model_daily is not None and not model_daily.empty:
        axes[0].plot(model_daily["date"], model_daily["wealth"], label="walk-forward ML", linewidth=1.8)
    axes[0].set_title("Out-of-sample portfolio wealth")
    axes[0].set_ylabel("wealth")
    axes[0].legend(frameon=False)
    axes[0].grid(alpha=0.2)

    for daily, label in ((factor_daily, "factor baseline"), (model_daily, "walk-forward ML")):
        if daily is not None and not daily.empty:
            wealth = daily["wealth"]
            drawdown = wealth / wealth.cummax() - 1.0
            axes[1].plot(daily["date"], drawdown, label=label, linewidth=1.5)
    axes[1].set_title("Drawdown")
    axes[1].set_ylabel("drawdown")
    axes[1].grid(alpha=0.2)
    axes[1].legend(frameon=False)
    fig.tight_layout()
    fig.savefig(output / "performance.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(results["factor_ic"].index, results["factor_ic"].rolling(21).mean(), label="factor 21D mean IC")
    if "model_ic" in results and not results["model_ic"].empty:
        ax.plot(results["model_ic"].index, results["model_ic"].rolling(21).mean(), label="ML 21D mean IC")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title("Rolling information coefficient")
    ax.set_ylabel("Spearman IC")
    ax.grid(alpha=0.2)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(output / "information_coefficient.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(results["factor_spread"].index, results["factor_spread"].cumsum(), label="factor top-minus-bottom")
    if "model_spread" in results and not results["model_spread"].empty:
        ax.plot(results["model_spread"].index, results["model_spread"].cumsum(), label="ML top-minus-bottom")
    ax.set_title("Cumulative quantile spread")
    ax.set_ylabel("cumulative forward return")
    ax.grid(alpha=0.2)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(output / "quantile_spread.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    summary = {
        "factor_baseline": results["factor_summary"],
        "walk_forward_ml": results.get("model_summary", {}),
    }
    (output / "metrics.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    _write_summary(summary, output / "summary.md", results["signal_name"])
    return results.get("model_summary") or results["factor_summary"]
