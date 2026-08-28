# Alpha Signal Research 项目设计规格

## 目标

在 ML 仓库中新增一个面向 Quantitative Strategist 面试与高校研究申请的旗舰项目。项目将把 Alpha 信号研究抽象为可复用、可比较、可迭代的研究框架：替换信号或模型后，自动沿用同一套数据、验证、组合、风险与报告流程。

## 研究问题

基于公开市场数据构造价格与成交量信号，研究其对未来横截面收益的预测能力，并评估信号在交易成本、组合约束和不同市场阶段下是否仍然稳健。

第一版固定实现四类信号：Momentum、Reversal、Volatility、Liquidity。第一版固定比较三个模型层次：等权因子基线、Ridge、树模型。深度学习不在本项目第一版中重复建设，而由仓库中的 DL 项目负责。

## 设计原则

1. 信号与组合、风险和报告解耦；信号只负责生成资产—日期级别的分数。
2. 所有实验使用统一的配置和结果 schema，保证不同信号可横向比较。
3. 时间序列验证优先，严格防止未来数据泄露；测试集只用于最终评估。
4. 结果同时报告预测能力与投资结果，不以单一净值曲线作为结论。
5. 以研究可解释性为优先，不建设低延迟交易系统或生产级基础设施。

## 研究流程

```text
数据与股票池
    → 特征与标签
    → 信号 / 模型
    → IC 与分组分析
    → Walk-forward 样本外预测
    → 组合构建
    → 成本与风险分析
    → 稳健性报告
```

## 目录与组件

```text
15_Alpha_Signal_Research/
├── README.md
├── requirements.txt
├── configs/
├── data/README.md
├── notebooks/
│   ├── 01_data_universe.ipynb
│   ├── 02_factor_construction.ipynb
│   ├── 03_factor_analysis.ipynb
│   ├── 04_ml_signal_model.ipynb
│   ├── 05_portfolio_backtest.ipynb
│   └── 06_robustness_report.ipynb
├── src/
│   ├── data.py
│   ├── features.py
│   ├── signals.py
│   ├── validation.py
│   ├── portfolio.py
│   ├── metrics.py
│   └── reporting.py
├── reports/
└── tests/
```

## 统一数据契约

核心研究表使用长表格式，至少包含：`date`、`asset`、`close`、`volume`、特征列、`forward_return`、`signal`、`weight`。信号函数接收特征表与配置，返回带有 `date`、`asset`、`signal` 的表；组合函数接收信号表与收益表，返回组合收益、权重和交易明细。

## 信号与模型

### 规则信号

- Momentum：过去 21、63、126、252 个交易日收益。
- Reversal：过去 5、20 个交易日收益的反向排名。
- Volatility：滚动波动率与波动率调整后的动量。
- Liquidity：成交量变化、换手代理指标和 Amihud 风格流动性指标。

所有因子在组合形成时使用滞后数据，并进行截面标准化与 winsorization。组合信号支持单因子、等权合成与配置权重合成。

### 预测模型

- Baseline：单因子与等权多因子。
- Linear：Ridge，展示正则化与可解释系数。
- Tree：HistGradientBoostingRegressor，展示非线性特征组合。

模型输出统一转为截面排名或预测收益，之后进入相同的组合与风险流程。

## 验证与风险控制

- 按时间进行训练、验证和测试，不使用随机切分。
- 使用滚动 Walk-forward 评估。
- 对重叠预测区间提供 Purged/Embargo 验证接口。
- 预测指标：Mean IC、Rank IC、IC Information Ratio、分组收益。
- 投资指标：年化收益、波动率、Sharpe、最大回撤、换手率、胜率。
- 成本分析：手续费与按换手率计的滑点敏感性。
- 风险分析：行业/风格暴露、子时期表现、因子相关性、组合集中度。
- 稳健性：持有周期、分组数量、成本假设、信号权重和市场阶段敏感性。

## GitHub 展示标准

README 首屏必须回答研究问题、数据范围、方法、主要结论与限制；提供一张研究流程图和一张结果总览图。Notebook 保留关键图表输出，代码放入小型 `src` 模块，测试覆盖标签滞后、时间切分、分组组合和指标计算。不得宣称真实可交易收益，也不得隐藏失败实验或数据限制。

## 成功标准

1. 新增一个信号只需实现统一接口或修改配置，不需改动回测和报告逻辑。
2. 一条命令可以运行演示数据并生成 HTML/PNG 研究结果。
3. 测试覆盖核心研究约束，并能在无网络环境运行。
4. 项目能够支持 10 分钟 QS 面试讲解：研究假设、信号机制、验证、组合化、风险与失败原因。
5. 项目同时具备研究报告形式，适合高校导师快速理解和进一步讨论。
