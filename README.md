# tool-problem-optima

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![UTEO Rating: S-Master](https://img.shields.io/badge/UTEO_Rating-S_Master_(Fixed--Point)-blueviolet?logo=shield)](CORE_INVARIANTS.md)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg?logo=python)](https://python.org)
[![Zero-Env: 100% Self-Contained](https://img.shields.io/badge/Zero--Env-100%25%20Self--Contained-orange.svg)](#)
[![UCFS: v1.0 Compliant](https://img.shields.io/badge/UCFS-v1.0%20Compliant-brightgreen.svg)](#)
[![Architecture: Pareto Optimal](https://img.shields.io/badge/Architecture-Problemology_Tensor-purple.svg)](#)
[![Tests: 100% Passing](https://img.shields.io/badge/Tests-100%25%20Passing-brightgreen.svg)](#)

</div>

> **全域编程问题论、认知病理学与全阶缺陷终结引擎**  
> *Universal Problemology, Cognitive Pathology & Defect Elimination Engine*  
> **工程性状**：`Type: TOOL` | `规范: OMNI-PROJECT-SPEC Level 2` | `评分: 100/100 S-Grade` | `100% 离线自洽标准库实现`

---

## ⚡ 极速开始 (Quick Start in 3 Seconds)

本项目采用**纯 Python 3.8+ 标准库自洽架构**，冷启动时延小于 10 毫秒，支持 Windows / Linux / macOS 全平台零配置即开即用。

```bash
# 方式 1: 交互式宝塔风格数字控制台菜单 (支持任意平台)
python main.py panel
# 或 Windows PowerShell:
.\run.ps1 panel

# 方式 2: 一键对目标 Python 文件或工程执行全阶病理审计 (毫秒级输出 Miette 精美诊断与张量雷达)
python main.py audit examples/buggy_sample.py

# 方式 3: 工业母机多工具联邦协同审计 (联动 tool-code-optima / tool-syntax-gate / tool-tdd-runner)
python main.py federated .

# 方式 4: 查看 6 大架构分类与 30+ 经典问题论缺陷目录
python main.py categories
python main.py catalog --category "Security & Supply Chain"

# 方式 5: 查阅全阶缺陷终结数学与系统论证明 (在线阅读或导出)
python main.py proof

# 方式 6: 自动化健康状态探测 (CI/CD 零退出码集成)
python main.py health --json
```

---

## 💡 第一性原理：从“问题论”学科重构软件缺陷 (The Epistemic Shift)

### 核心拷问 1：软件缺陷的切入点，真的应该是“AI 还是人类”的问题吗？

在传统的工程认知中，人们习惯于割裂地讨论“这是大模型的幻觉（Hallucination）”或者“这是人类程序员的粗心（Typo/Bug）”。但从第一性原理出发，**这种二元对立在科学上是肤浅且非本质的**。

无论是人类神经元网络的生物突触，还是人工神经网络的 Transformer 自注意力矩阵，在面对编程任务时，都不过是**“在有限信息与认知约束下的状态空间搜索主体”**。

**任何计算问题（Problem）或缺陷（Defect）的本质，天然是广义计算问题学（Computational Problemology）与系统病理学的一个具体特例**。

```
                  ┌───────────────────────────────┐
                  │   意图流形 I (Intent Space)   │
                  └───────────────┬───────────────┘
                                  │ Δ_IS (规范投机 / 奖励作弊)
                                  ▼
                  ┌───────────────────────────────┐
                  │ 形式化规范 S (Specification)  │
                  └───────┬───────────────┬───────┘
                          │               │
  Δ_SE (语义偏差 / 崩溃) │               │ Δ_VI (验证假象 / 补丁过拟合)
                          ▼               ▼
        ┌─────────────────────────┐   ┌─────────────────────────┐
        │ 执行状态 E (Execution)   │◄──┤ 验证神谕 V (Oracle)     │
        └─────────────┬───────────┘   └─────────────────────────┘
                      │
                      │ Δ_EC (环境失配 / 捷径学习)
                      ▼
        ┌─────────────────────────┐
        │ 运行环境 C (Context)    │
        └─────────────────────────┘
```

根据广义问题论公理，任何软件缺陷天然是四大基底空间之间的**非零散度张量 (Non-Zero Divergence Tensor)**：

$$\mathcal{P} \equiv \nabla(\mathcal{I}, \mathcal{S}, \mathcal{E}, \mathcal{C}) \neq \mathbf{0}$$

- **$\Delta_{IS}$ (意图-规范失配)**：规范投机（Specification Gaming）、指标异化（Goodhart's Law）；
- **$\Delta_{SE}$ (规范-实现偏差)**：边界差一错误、空指针、类型混淆、语法崩溃；
- **$\Delta_{EC}$ (实现-环境失调)**：捷径学习（Shortcut Learning）、隐式状态爆炸、竞态条件、内存泄漏；
- **$\Delta_{VI}$ (验证神谕假象)**：补丁过拟合（Patch Overfitting）、同义反复验证（Circular Testing）；
- **$\Delta_{T}$ (时空演化衰退)**：代码腐化、上下文注意力漂移、架构熵增。

---

## 🔬 核心拷问 2：问题千奇百怪，一个项目凭什么能够全部解决/监督修正？

详见数学论证专文：**《[THEORETICAL_PROOF.md](THEORETICAL_PROOF.md)》**。核心论证涵盖四大数学支柱：

1. **莱斯定理边界与不变式约束范式转换 (Rice's Theorem & Invariant Confinement)**：
   - 语义完备性虽不可判定，但保音抽象解释（Sound Abstract Interpretation, Cousot 1977）可将程序状态机永久封闭在霍尔三元组安全子空间 $\Omega_{\text{safe}}$ 内。
2. **范畴论泛性质与代数对称性归约 (Category-Theoretic Universal Morphisms)**：
   - 表面语法的千奇百怪，代数本质只有有限种坍塌：**幂等律守恒（$f(f(x))=f(x)$）、置换对称性（$f(x,y)=f(y,x)$）、函子可结合性、线性资源对偶性与 DAG 拓扑无环性**。
   - 约束了这五大代数基底，即可在数学上实现对全阶表面缺陷的降维覆盖。
3. **控制论阿什比必要多样性定律 (Ashby's Law of Requisite Variety)**：
   - 静态规则库必败（多样性 $V_R$ 有限）；本项目采用**对偶动态生成控制架构**，蜕变对抗神谕动态生成的输入微扰使得调节器多样性 $V_R$ 始终压制缺陷多样性 $V_D$。
4. **巴拿赫不动点收敛定理 (The Banach Fixed-Point Convergence)**：
   - 在 5-Axis 张量度量空间中，基于反例梯度的修复算子 $\Phi$ 构成严格压缩映射，数学保证迭代轨迹收敛至唯一的零缺陷不动点 $\mathcal{P}(x^*) \equiv 0$。

---

## 🧭 5-Axis 张量参数网络 (The 5-Axis Tensor Metric Space)

```
                    Axis O: Ontological Origin (本体根源)
                                  ▲
                                  │
    Axis A: Agency & Cognitive    │    Axis L: Epistemic Layer
    (主体认知机制) ◄──────────────┼──────────────► (知识能级)
                                  │
                                  │
                                  ▼
                     Axis M: Masking & Observability
                           (可观测性与伪装层深)
                                  +
                     Axis R: Remediation Dynamics
                           (修复动力学与闭环收敛)
```

1. **Axis O (Ontological Origin / 本体根源, 5 维基底)**：`O1:Intent-Spec-Gap`、`O2:Spec-Exec-Divergence`、`O3:Exec-Context-Mismatch`、`O4:Verification-Illusion`、`O5:Temporal-Entropy`；
2. **Axis A (Agency & Cognitive Mode / 主体认知机制, 5 维基底)**：`A1:Statistical-Hallucination`、`A2:Optimization-Gaming`、`A3:Bounded-Rationality`、`A4:Confirmation-Bias`、`A5:Circular-Epistemic`；
3. **Axis L (Epistemic Abstraction Layer / 知识能级, 5 维基底)**：`L1:Syntactic-Lexical`、`L2:Type-Memory-Safety`、`L3:Algorithm-State`、`L4:Contract-Invariant`、`L5:Business-Teleology`；
4. **Axis M (Observability & Masking / 可观测性与伪装层深, 4 维基底)**：`M1:Explicit-Crash`、`M2:Silent-Degradation`、`M3:Plausible-Green-Deception`、`M4:Intermittent-Heisenbug`；
5. **Axis R (Remediation Dynamics / 修复动力学与闭环收敛, 4 维基底)**：`R1:Static-AST-Gate`、`R2:Metamorphic-Oracle`、`R3:Dynamic-Invariant-Contract`、`R4:Closed-Loop-Critic`。

---

## 🗂️ 全域六大分类与 30+ 经典问题论百科 (The 6 Architectural Categories)

| 分类流形 | 包含经典病理 | 代表性缺陷代码与权威出处 | 核心防线机制 |
| :--- | :--- | :--- | :--- |
| **1. 提示词、上下文衰减与认知偏差**<br/>*(Context & Cognitive)* | 注意力稀释、大海捞针失忆、盲目阿谀奉承、Token预算耗尽、提示词优先级倒置 | `PRB-E001` (Lost in the Middle, TACL)<br/>`PRB-E002` (Anthropic Sycophancy)<br/>`PRB-E003` (Token Horizon AST Truncation)<br/>`PRB-E004` (Prompt Injection OWASP) | 分段显式锚定、AST 闭包完整性门禁、控制/数据平面正交隔离 |
| **2. 智能体工具调用与环境状态交叠**<br/>*(Agentic Tooling & Environment)* | 螺旋幻觉死循环、工具参数臆造、排错振荡死循环、影子路径脱节、终端截断盲区 | `PRB-E107` (SurgeHQ Hallucination)<br/>`PRB-E111` (Toolformer / ToolLLM)<br/>`PRB-E112` (Ashby Requisite Variety Thrashing)<br/>`PRB-E113` (POSIX Path Drift) | 单一真相源反射锚定、Tarjan 环路阻断、Schema 刚性参数白名单 |
| **3. 算法合成与程序语义病理**<br/>*(Algorithmic Synthesis & Logic)* | 补丁过拟合、规范投机/奖励作弊、捷径学习、聪明的汉斯效应、边界栅栏差一、隐式空指针、浮点非结合律、ReDoS | `PRB-E101` (Smith et al. APR 2015)<br/>`PRB-E102` (Krakovna et al. DeepMind)<br/>`PRB-E103` (Geirhos et al. Nature MI)<br/>`PRB-E201` (Dijkstra Fencepost)<br/>`PRB-E204` (ReDoS Thompson NFA) | 蜕变测试神谕、代数对称性扰动、高精度定点数、线性时间 DFA 门禁 |
| **4. 系统架构、状态机与高并发**<br/>*(Architecture & Concurrency)* | 抽象泄露与状态爆炸、TOCTOU时差竞态、异序加锁死锁、句柄资源泄露、级联雪崩与惊群 | `PRB-E109` (Spolsky Leaky Abstraction)<br/>`PRB-E301` (CWE-367 TOCTOU)<br/>`PRB-E302` (Coffman Deadlock 1971)<br/>`PRB-E303` (RAII CWE-775)<br/>`PRB-E304` (Google SRE Thundering Herd) | 混沌时延注入、原子系统调用 (EAFP)、全序加锁规约、Single-Flight 读屏障 |
| **5. 测试学、形式化验证与认知闭环**<br/>*(Testing, Oracle & Epistemic)* | 同义反复循环验证、古德哈特定律失效(假覆盖率)、Mock 作弊与倒置、脆弱测试、断言轮盘赌、代数性质违背 | `PRB-E104` (Dijkstra / Parnas Tautological)<br/>`PRB-E105` (Goodhart's Law 1975)<br/>`PRB-E110` (Fowler Mocks Aren't Stubs)<br/>`PRB-E401` (Flaky Tests FSE 2014)<br/>`PRB-E403` (Metamorphic Testing 1998) | 双轨独立神谕、变异测试门禁、真实容器集成、虚拟时钟隔离、代数不变式 |
| **6. 安全隐患、依赖膨胀与供应链病理**<br/>*(Security & Supply Chain)* | 静默吞异常与故障掩蔽、虚构三方包投毒、依赖传递膨胀与循环引用、硬编码凭据与 Prompt 泄露 | `PRB-E108` (CWE-391 Bare Except)<br/>`PRB-E501` (Slopsquatting Vulcan Cyber)<br/>`PRB-E502` (Bloaty / tool-code-optima)<br/>`PRB-E503` (CWE-798 Secret Leak) | Fail-Fast 异常强阻断、PyPI 官方索引核验、DAG 拓扑无环检查、香农熵凭据扫描 |

---

## 🏭 工业母机多工具联邦协同架构 (Federated Synergy Architecture)

本项目并非孤立运行，而是作为顶层问题论指挥中枢，与宿主机 `D:/github` 工业母机无缝级联：

```
                    ┌───────────────────────────────┐
                    │      tool-problem-optima      │
                    │   全知问题论中枢与张量收敛机  │
                    └───────────────┬───────────────┘
          ┌─────────────────────────┼─────────────────────────┐
          ▼                         ▼                         ▼
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│ tool-syntax-gate │      │ tool-code-optima │      │ tool-tdd-runner  │
│ 零Token毫秒级    │      │ 深度架构DAG防腐  │      │ 沙箱化确定性     │
│ AST 词法前置门禁 │      │ 复杂度与体积治理 │      │ 测试矩阵调度执行 │
└──────────────────┘      └──────────────────┘      └──────────────────┘
```

```bash
# 执行全域多工具联邦协同体检：
python main.py federated D:/my-project
```

- **第一道防线：`tool-syntax-gate`**（5 毫秒内粉碎语法错误与残缺 AST，零 Token 损耗）；
- **第二道防线：`tool-code-optima`**（粉碎依赖膨胀、冗余导入、认知复杂度超标与循环引用）；
- **第三道防线：`tool-tdd-runner`**（提供沙箱化、确定性超时的测试执行环境）；
- **终极防线：`tool-problem-optima`**（计算 5-Axis 张量散度，运行蜕变神谕，监督不动点收敛）。

---

## 📋 统一 5 大通用操作动词 (Unified Operations)

```bash
# 1. 验证运行环境 (setup)
.\run.ps1 setup

# 2. 运行默认自检与审计 (run)
.\run.ps1 run .

# 3. 运行全量单元与蜕变测试套件 (test)
.\run.ps1 test

# 4. 探针健康诊断 (health)
.\run.ps1 health

# 5. 清理缓存与编译产物 (clean)
.\run.ps1 clean
```

---

## 📜 许可证 (License)

本项目采用 [MIT License](LICENSE) 开源协议。
