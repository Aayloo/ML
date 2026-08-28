import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from run_demo import run_demo


def test_demo_runner_creates_a_summary_and_figures(tmp_path):
    result = run_demo(output_dir=tmp_path, signal_name="momentum")

    assert (tmp_path / "summary.md").exists()
    assert (tmp_path / "performance.png").exists()
    assert "sharpe" in result
