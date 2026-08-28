# Alpha Signal Research Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reproducible, modular Alpha Signal Research flagship project for Quantitative Strategist interview preparation and academic research presentation.

**Architecture:** A small Python research package separates data generation/loading, feature and signal construction, walk-forward validation, portfolio formation, metrics, and reporting. Signals share one interface and feed the same analysis pipeline, so changing a signal or configuration regenerates comparable outputs.

**Tech Stack:** Python 3.10+, NumPy, Pandas, scikit-learn, Matplotlib, Jupyter, pytest.

**Spec:** `docs/superpowers/specs/2026-08-28-alpha-signal-research-design.md`

## Global Constraints

- The project must run offline with deterministic demo data.
- No random train/test split; all evaluation is time ordered.
- Features must be lagged relative to forward-return labels.
- Reports must include predictive and portfolio metrics, costs, turnover, and drawdown.
- The project must not claim live or guaranteed investment performance.
- Deep learning, low-latency execution, and production trading infrastructure are out of scope.

---

### Task 1: Create research package contracts and offline data fixture

**Files:**
- Create: `15_Alpha_Signal_Research/src/__init__.py`
- Create: `15_Alpha_Signal_Research/src/data.py`
- Create: `15_Alpha_Signal_Research/tests/test_data.py`
- Create: `15_Alpha_Signal_Research/requirements.txt`
- Create: `15_Alpha_Signal_Research/data/README.md`

**Interfaces:**
- `make_demo_market_data(n_days: int = 520, n_assets: int = 24, seed: int = 7) -> pandas.DataFrame`
- Returned columns: `date`, `asset`, `close`, `volume`.

- [ ] **Step 1: Write the failing tests**

```python
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
```

- [ ] **Step 2: Run the tests and verify they fail because `src.data` is missing**

Run: `pytest 15_Alpha_Signal_Research/tests/test_data.py -q`

- [ ] **Step 3: Implement deterministic synthetic market data and dependency file**

- [ ] **Step 4: Run the focused tests and verify they pass**

Run: `pytest 15_Alpha_Signal_Research/tests/test_data.py -q`

- [ ] **Step 5: Commit**

```bash
git add 15_Alpha_Signal_Research
git commit -m "feat: scaffold alpha research data contract"
```

### Task 2: Implement lagged features and pluggable Alpha signals

**Files:**
- Create: `15_Alpha_Signal_Research/src/features.py`
- Create: `15_Alpha_Signal_Research/src/signals.py`
- Create: `15_Alpha_Signal_Research/tests/test_features_signals.py`
- Create: `15_Alpha_Signal_Research/configs/baseline.json`

**Interfaces:**
- `build_features(market_data: pandas.DataFrame, config: dict) -> pandas.DataFrame`
- `build_signal(feature_data: pandas.DataFrame, name: str, config: dict) -> pandas.DataFrame`
- Signal output columns: `date`, `asset`, `signal`.

- [ ] **Step 1: Write failing tests for lagging and signal registry**

```python
def test_forward_return_is_not_available_as_a_feature():
    features = build_features(make_demo_market_data(80, 4), {"horizon": 5})
    assert "forward_return" in features.columns
    assert "forward_return" not in {c for c in features.columns if c.endswith("_feature")}

def test_all_signal_names_return_the_same_contract():
    features = build_features(make_demo_market_data(80, 4), {"horizon": 5})
    for name in ("momentum", "reversal", "volatility", "liquidity"):
        result = build_signal(features, name, {})
        assert list(result.columns) == ["date", "asset", "signal"]
        assert result["signal"].notna().any()
```

- [ ] **Step 2: Run focused tests and verify the expected missing-function failures**

Run: `pytest 15_Alpha_Signal_Research/tests/test_features_signals.py -q`

- [ ] **Step 3: Implement cross-sectional winsorization, lagged features, four signals, and signal registry**

- [ ] **Step 4: Run focused tests and verify they pass**

Run: `pytest 15_Alpha_Signal_Research/tests/test_features_signals.py -q`

- [ ] **Step 5: Commit**

```bash
git add 15_Alpha_Signal_Research/src/features.py 15_Alpha_Signal_Research/src/signals.py 15_Alpha_Signal_Research/tests/test_features_signals.py 15_Alpha_Signal_Research/configs/baseline.json
git commit -m "feat: add lagged features and pluggable alpha signals"
```

### Task 3: Add time-ordered validation and predictive metrics

**Files:**
- Create: `15_Alpha_Signal_Research/src/validation.py`
- Create: `15_Alpha_Signal_Research/src/metrics.py`
- Create: `15_Alpha_Signal_Research/tests/test_validation_metrics.py`

**Interfaces:**
- `walk_forward_splits(dates: Sequence, train_size: int, test_size: int, step: int) -> Iterator[tuple[set, set]]`
- `cross_sectional_ic(frame: pandas.DataFrame, signal_col: str = "signal", target_col: str = "forward_return") -> pandas.Series`
- `performance_summary(returns: pandas.Series, periods_per_year: int = 252) -> dict`

- [ ] **Step 1: Write failing tests for chronological splits, IC, and drawdown**

```python
def test_walk_forward_splits_never_train_on_future_dates():
    dates = pd.date_range("2020-01-01", periods=10, freq="D")
    splits = list(walk_forward_splits(dates, train_size=5, test_size=2, step=2))
    assert splits
    for train_dates, test_dates in splits:
        assert max(train_dates) < min(test_dates)

def test_performance_summary_reports_drawdown_and_sharpe_keys():
    summary = performance_summary(pd.Series([0.01, -0.02, 0.01]))
    assert {"annualized_return", "annualized_volatility", "sharpe", "max_drawdown"} <= summary.keys()
```

- [ ] **Step 2: Run focused tests and verify they fail for the missing interfaces**

Run: `pytest 15_Alpha_Signal_Research/tests/test_validation_metrics.py -q`

- [ ] **Step 3: Implement chronological splits, cross-sectional IC, and performance statistics**

- [ ] **Step 4: Run focused tests and verify they pass**

Run: `pytest 15_Alpha_Signal_Research/tests/test_validation_metrics.py -q`

- [ ] **Step 5: Commit**

```bash
git add 15_Alpha_Signal_Research/src/validation.py 15_Alpha_Signal_Research/src/metrics.py 15_Alpha_Signal_Research/tests/test_validation_metrics.py
git commit -m "feat: add walk-forward validation and alpha metrics"
```

### Task 4: Implement portfolio construction, costs, and robustness outputs

**Files:**
- Create: `15_Alpha_Signal_Research/src/portfolio.py`
- Create: `15_Alpha_Signal_Research/src/reporting.py`
- Create: `15_Alpha_Signal_Research/tests/test_portfolio.py`

**Interfaces:**
- `rank_portfolio(signal_frame: pandas.DataFrame, n_quantiles: int = 5, long_short: bool = True) -> pandas.DataFrame`
- `backtest(signal_frame: pandas.DataFrame, returns: pandas.DataFrame, cost_bps: float = 5.0) -> pandas.DataFrame`
- `save_report(results: dict, output_dir: pathlib.Path) -> dict`

- [ ] **Step 1: Write failing tests for weight neutrality, costs, and turnover**

```python
def test_long_short_portfolio_is_cross_sectionally_neutral():
    weights = rank_portfolio(sample_signals(), n_quantiles=3, long_short=True)
    daily = weights.groupby("date")["weight"].sum()
    assert (daily.abs() < 1e-9).all()

def test_transaction_costs_reduce_net_returns():
    result = backtest(sample_signals(), sample_returns(), cost_bps=10)
    assert (result["net_return"] <= result["gross_return"]).all()
```

- [ ] **Step 2: Run focused tests and verify they fail for the missing portfolio interfaces**

Run: `pytest 15_Alpha_Signal_Research/tests/test_portfolio.py -q`

- [ ] **Step 3: Implement rank-based portfolio weights, turnover, costs, and report plotting**

- [ ] **Step 4: Run focused tests and verify they pass**

Run: `pytest 15_Alpha_Signal_Research/tests/test_portfolio.py -q`

- [ ] **Step 5: Commit**

```bash
git add 15_Alpha_Signal_Research/src/portfolio.py 15_Alpha_Signal_Research/src/reporting.py 15_Alpha_Signal_Research/tests/test_portfolio.py
git commit -m "feat: add portfolio construction and cost-aware backtest"
```

### Task 5: Add offline demo runner, research notebooks, and GitHub-facing documentation

**Files:**
- Create: `15_Alpha_Signal_Research/run_demo.py`
- Create: `15_Alpha_Signal_Research/README.md`
- Create: `15_Alpha_Signal_Research/notebooks/01_data_universe.ipynb`
- Create: `15_Alpha_Signal_Research/notebooks/02_factor_construction.ipynb`
- Create: `15_Alpha_Signal_Research/notebooks/03_factor_analysis.ipynb`
- Create: `15_Alpha_Signal_Research/notebooks/04_ml_signal_model.ipynb`
- Create: `15_Alpha_Signal_Research/notebooks/05_portfolio_backtest.ipynb`
- Create: `15_Alpha_Signal_Research/notebooks/06_robustness_report.ipynb`
- Create: `15_Alpha_Signal_Research/reports/.gitkeep`

- [ ] **Step 1: Write a smoke test for the offline runner**

```python
def test_demo_runner_creates_a_summary_and_figures(tmp_path):
    result = run_demo(output_dir=tmp_path, signal_name="momentum")
    assert (tmp_path / "summary.md").exists()
    assert (tmp_path / "performance.png").exists()
    assert "sharpe" in result
```

- [ ] **Step 2: Run the smoke test and verify it fails because the runner is missing**

Run: `pytest 15_Alpha_Signal_Research/tests/test_runner.py -q`

- [ ] **Step 3: Implement the runner, notebooks, README, research workflow diagram, and output links**

- [ ] **Step 4: Run the smoke test and verify it passes**

Run: `pytest 15_Alpha_Signal_Research/tests/test_runner.py -q`

- [ ] **Step 5: Commit**

```bash
git add 15_Alpha_Signal_Research
git commit -m "docs: publish alpha signal research flagship project"
```

### Task 6: Full verification and GitHub synchronization

**Files:**
- Modify: `15_Alpha_Signal_Research/README.md` if verification exposes incorrect commands or claims.

- [ ] **Step 1: Run the full test suite**

Run: `pytest 15_Alpha_Signal_Research/tests -q`

- [ ] **Step 2: Run the offline demo from the project directory**

Run: `python run_demo.py --signal momentum --output-dir reports/demo`

- [ ] **Step 3: Inspect generated files and Git diff**

Run: `Get-ChildItem -Recurse reports\demo; git diff --check; git status --short`

- [ ] **Step 4: Commit the verified implementation**

```bash
git add 15_Alpha_Signal_Research
git commit -m "feat: complete quantitative strategist alpha research project"
```

- [ ] **Step 5: Push the verified commits to GitHub**

```bash
git push origin main
```
