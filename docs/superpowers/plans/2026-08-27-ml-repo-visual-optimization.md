# ML Repository Visual Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the repository homepage into a polished, visual ML learning hub, temporarily archive chapters 15–17 without deleting them, and make the chapter experiments easier to interpret and reproduce.

**Architecture:** Keep the existing numbered Notebook layout and Git history. Add a single static SVG plus a Markdown companion as the documentation source of truth, use README as the public landing page, and move late-stage chapters under `archive/` with all links updated. Apply only targeted Notebook changes that improve navigation or prevent misleading evaluation claims.

**Tech Stack:** Markdown, GitHub-flavored Mermaid, hand-authored SVG, Jupyter Notebook JSON, Python standard library, scikit-learn, pandas, and existing repository dependencies.

**Spec:** `docs/superpowers/specs/2026-08-27-ml-repo-optimization-design.md`

## Global Constraints

- Preserve all Notebook content; chapters 15–17 are moved to `archive/` and are not deleted.
- Do not rewrite the existing Git history or force-push rewritten commits.
- The public main path is chapters 01–14; the README must clearly expose the archive instead of pretending those chapters do not exist.
- ML evaluation language must distinguish exploratory full-data visualizations from train-only fitted transforms and must not present financial demonstrations as investment advice.
- Use the existing Python dependency set; do not add a framework solely for rendering the route map.

---

### Task 1: Add the visual roadmap and quality guide

**Files:**
- Create: `docs/learning-roadmap.svg`
- Create: `docs/learning-roadmap.md`
- Create: `docs/ml-quality-checklist.md`

**Interfaces:**
- `README.md` will embed `docs/learning-roadmap.svg` and link to `docs/learning-roadmap.md`.
- Every roadmap chapter node must point to the current repository path, including `archive/15_图像分类/...`, `archive/16_量化ML/...`, and `archive/17_文本分类/...` after Task 3.

- [ ] **Step 1: Write the Markdown roadmap content**

  Include one Mermaid flowchart with these stages and links: `01 线性回归 → 02 逻辑回归 → 03 决策树 → 04 朴素贝叶斯 → 05 SVM → 06 KNN → 07 K-Means → 08 综合案例 → 09 集成学习 → 10 PCA → 11 核方法 → 12 特征工程与模型选择 → 13 综合项目 → 14 金融回归`; branch after 14 to archived `15 图像分类`, `16 量化 ML`, and `17 文本分类`. Add prerequisites and a “通过标准” section with one concrete outcome for each stage.

- [ ] **Step 2: Create the static SVG**

  Create a 1600×900 SVG with a dark navy background, a restrained blue/teal/orange palette, a title, a four-stage horizontal flow, numbered rounded cards, branch cards for 13–14, and a dashed archive section for 15–17. Each card must include a short label and a visible sequence number. Use plain SVG text and shapes so GitHub renders it without a build step.

- [ ] **Step 3: Write the quality checklist**

  Cover: problem definition, baseline, provenance, train/validation/test separation, `Pipeline`, leakage checks, metric choice, error analysis, random seeds, i.i.d. versus time-series validation, backtest rules, and the project’s “educational demonstration, not production or investment advice” boundary.

- [ ] **Step 4: Verify the new docs are internally linked**

  Run:

  ```powershell
  rg -n "01_|02_|03_|04_|05_|06_|07_|08_|09_|10_|11_|12_|13_|14_|15_|16_|17_" docs/learning-roadmap.md
  ```

  Expected: all 17 chapter identifiers appear, with 15–17 using `archive/` paths after Task 3.

- [ ] **Step 5: Commit**

  ```powershell
  git add docs/learning-roadmap.svg docs/learning-roadmap.md docs/ml-quality-checklist.md
  git commit -m "docs: add visual ML roadmap and quality guide"
  ```

### Task 2: Rebuild the public README landing page

**Files:**
- Modify: `README.md`

**Interfaces:**
- The README embeds `docs/learning-roadmap.svg`, links to the Markdown roadmap and quality guide, and links every active chapter to its Notebook.

- [ ] **Step 1: Replace the long arrow-only route with a landing-page structure**

  Use these sections in order: project title and one-sentence promise; visual roadmap; “how to use this repository”; active curriculum 01–14; archived chapters 15–17; reproducible setup; data sources and licenses; ML quality standards; limitations and contribution note.

- [ ] **Step 2: Correct all counts and labels**

  State that the repository contains 18 Notebooks (`00–17`), with `00` as the detailed guide and `01–17` as 17 course/project chapters. State that the current public learning path is `01–14` and that `15–17` are archived temporarily.

- [ ] **Step 3: Add direct GitHub links**

  Use URL-encoded relative links for Chinese paths, and ensure each active row links to the Notebook file rather than only to a folder. Keep the archive visible as a recovery path.

- [ ] **Step 4: Commit**

  ```powershell
  git add README.md
  git commit -m "docs: redesign repository landing page"
  ```

### Task 3: Archive chapters 15–17 without deleting content

**Files:**
- Move: `15_图像分类/` → `archive/15_图像分类/`
- Move: `16_量化ML/` → `archive/16_量化ML/`
- Move: `17_文本分类/` → `archive/17_文本分类/`
- Modify: all README, Markdown, and Notebook references affected by the move

**Interfaces:**
- Existing Notebook filenames and data files remain unchanged inside the new archive paths.
- README and roadmap links must resolve to the moved files.

- [ ] **Step 1: Resolve and inspect targets**

  Run:

  ```powershell
  Get-ChildItem -LiteralPath '15_图像分类','16_量化ML','17_文本分类' -Force
  ```

  Expected: each target contains its Notebook and any required data files; no unrelated directory is selected.

- [ ] **Step 2: Move the directories with Git-aware renames**

  ```powershell
  New-Item -ItemType Directory -Force -Path archive | Out-Null
  git mv '15_图像分类' 'archive/15_图像分类'
  git mv '16_量化ML' 'archive/16_量化ML'
  git mv '17_文本分类' 'archive/17_文本分类'
  ```

- [ ] **Step 3: Update path references**

  Search all tracked text and Notebook sources for the old paths and replace only references to the moved chapters. Validate that no old top-level path remains in documentation.

- [ ] **Step 4: Commit**

  ```powershell
  git add -A
  git commit -m "chore: archive chapters 15 through 17"
  ```

### Task 4: Standardize chapter navigation and targeted Notebook semantics

**Files:**
- Modify: `00_机器学习模型路线图.ipynb`
- Modify: `01_线性回归/01_linear_regression.ipynb` through `14_金融回归/14_btc_return_regression.ipynb`
- Modify: `archive/15_图像分类/15_fashion_mnist.ipynb`, `archive/16_量化ML/16_quant_ml_factor.ipynb`, `archive/17_文本分类/17_text_classification.ipynb`

**Interfaces:**
- Each Notebook’s first non-empty Markdown cell starts with a compact navigation line linking to `README.md` and `docs/learning-roadmap.md`.
- Notebook code remains executable JSON; no new runtime package is introduced.

- [ ] **Step 1: Add the shared navigation line**

  Insert this Markdown prefix in each Notebook’s first non-empty Markdown cell, preserving its existing title immediately after it:

  ```markdown
  > [返回仓库首页](../README.md) · [查看可视化学习路线](../docs/learning-roadmap.md)
  ```

  For archived notebooks use `../../README.md` and `../../docs/learning-roadmap.md`.

- [ ] **Step 2: Correct the `00` guide counts**

  Replace claims that conflict with the repository: `00–17` means 18 Notebooks; `01–17` means 17 course/project chapters; 15–17 are temporarily archived. Keep the long-form references, but point readers to `docs/learning-roadmap.md` for the visual entrypoint.

- [ ] **Step 3: Fix 14-chapter target preprocessing**

  Replace the global target clipping block:

  ```python
  lo, hi = data["y_fwd5"].quantile(0.01), data["y_fwd5"].quantile(0.99)
  data["y_fwd5"] = data["y_fwd5"].clip(lo, hi)
  ```

  with a comment and implementation that leaves the forward target un-clipped for evaluation, while clipping only lagged return features already available at prediction time. Update the surrounding Markdown to say that target clipping is intentionally omitted to avoid using future-distribution quantiles.

- [ ] **Step 4: Clarify exploratory transforms in 13, 15, and 16**

  Add Markdown before the full-data PCA/KMeans sections stating that those fits are exploratory visualizations and are not used to claim held-out predictive performance. Keep the train-only scaler/model path as the strict evaluation path.

- [ ] **Step 5: Make 17-chapter CV deterministic**

  Replace the bare `cv=5` in the text classification `cross_validate` call with:

  ```python
  from sklearn.model_selection import StratifiedKFold

  cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
  res = cross_validate(model, X_train, y_train, cv=cv, scoring=scoring)
  ```

- [ ] **Step 6: Separate 16-chapter selection from final evaluation**

  Add an explicit time cutoff before the model-ranking loop: rank models only on the development period, then evaluate the selected model and fixed baselines on the final untouched period. Preserve the existing rolling-train logic and report the cutoff, number of periods, transaction cost, benchmark, and final evaluation window in the output summary.

- [ ] **Step 7: Commit**

  ```powershell
  git add -A
  git commit -m "fix: clarify notebook navigation and evaluation boundaries"
  ```

### Task 5: Validate the repository and review the final diff

**Files:**
- Test: all tracked `*.ipynb` files, `scripts/download_fashion_mnist.py`, Markdown/SVG links

- [ ] **Step 1: Validate Notebook JSON and script compilation**

  ```powershell
  $env:PYTHONIOENCODING='utf-8'
  @'
  import json, pathlib
  files = sorted(pathlib.Path('.').rglob('*.ipynb'))
  for path in files:
      json.loads(path.read_text(encoding='utf-8'))
  print(f'Notebook JSON valid: {len(files)} files')
  '@ | python -
  python -m compileall -q scripts
  ```

  Expected: `Notebook JSON valid: 18 files` and exit code 0.

- [ ] **Step 2: Check path integrity**

  Verify every Markdown link target exists, confirm `archive/15_图像分类`, `archive/16_量化ML`, and `archive/17_文本分类` exist, and confirm the old top-level directories no longer exist.

- [ ] **Step 3: Execute selected high-risk notebooks**

  Execute 14 and 16 in a temporary output directory with the existing environment. If a dependency or data download is unavailable, record the exact missing dependency/path and still run the static checks. Do not claim the notebooks passed without reading the execution exit code.

- [ ] **Step 4: Inspect the final diff and history**

  ```powershell
  git status --short
  git diff --stat HEAD~4..HEAD
  git log --oneline --decorate -8
  ```

  Confirm no Notebook or data file was accidentally deleted, the archive move is recoverable, and all new commits use meaningful types.

- [ ] **Step 5: Verify GitHub authentication and push**

  ```powershell
  & 'C:\Program Files\GitHub CLI\gh.exe' auth status
  git push origin main
  ```

  Expected: authenticated account `Aayloo`, push succeeds, and the remote branch contains the new commits. If authentication still reports an invalid token, stop before pushing and ask the user to rerun `gh auth login` in the same environment.
