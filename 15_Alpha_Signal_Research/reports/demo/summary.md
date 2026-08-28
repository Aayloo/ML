# Alpha Signal Research — Offline Demo

**Primary signal:** `momentum`

This report is generated from deterministic synthetic data for pipeline validation. It is not evidence of live-market performance.

## Performance summary

| Model | Annualized return | Volatility | Sharpe | Max drawdown |
|---|---:|---:|---:|---:|
| factor_baseline | 10.58% | 10.72% | 0.99 | -10.21% |
| walk_forward_ml | 2.34% | 10.94% | 0.27 | -16.87% |

## Research caveats

- Replace the demo loader with licensed point-in-time data before drawing investment conclusions.
- Keep the final test period untouched during feature and model selection.
- Re-estimate costs, liquidity, universe membership, and risk controls for any real deployment.
