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

# 方式 3: 查看 5-Axis 问题张量雷达图与形式化不变式
python main.py tensor PRB-E101

# 方式 4: 浏览全域经典软件病理学与 AI 缺陷百科全书
python main.py catalog

# 方式 5: 自动化健康状态探测 (CI/CD 零退出码集成)
python main.py health --json
```

---

## 💡 第一性原理：从“问题论”学科重构软件缺陷 (The Epistemic Shift)

### 核心拷问：软件缺陷的切入点，真的应该是“AI 还是人类”的问题吗？

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

## 🧭 5-Axis 张量参数网络 (The 5-Axis Tensor Metric Space)

为了对千奇百怪的问题建立可量化、可计算的几何拓扑，本项目建立了正交的 5-Axis 张量投影网络：

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

1. **Axis O (Ontological Origin / 本体根源, 5 维基底)**：
   - `O1:Intent-Spec-Gap`（意图-规范失配）
   - `O2:Spec-Exec-Divergence`（规范-实现偏差）
   - `O3:Exec-Context-Mismatch`（实现-环境失调）
   - `O4:Verification-Illusion`（验证神谕假象）
   - `O5:Temporal-Entropy`（时空演化衰退）
2. **Axis A (Agency & Cognitive Mode / 主体认知机制, 5 维基底)**：
   - `A1:Statistical-Hallucination`（统计型虚构）
   - `A2:Optimization-Gaming`（目标投机与捷径）
   - `A3:Bounded-Rationality`（有限理性与过载）
   - `A4:Confirmation-Bias`（确认偏误与盲区）
   - `A5:Circular-Epistemic`（同义反复与循环自洽）
3. **Axis L (Epistemic Abstraction Layer / 知识能级, 5 维基底)**：
   - `L1:Syntactic-Lexical`（句法与词法级）
   - `L2:Type-Memory-Safety`（类型与内存边界级）
   - `L3:Algorithm-State`（算法与状态机级）
   - `L4:Contract-Invariant`（契约与不变式级）
   - `L5:Business-Teleology`（业务意图与系统目标级）
4. **Axis M (Observability & Masking / 可观测性与伪装层深, 4 维基底)**：
   - `M1:Explicit-Crash`（立即暴露崩溃）
   - `M2:Silent-Degradation`（静默腐化/泄漏）
   - `M3:Plausible-Green-Deception`（伪绿假象：测试全过但逻辑彻底失效）
   - `M4:Intermittent-Heisenbug`（测不准/偶发竞态）
5. **Axis R (Remediation Dynamics / 修复动力学与闭环收敛, 4 维基底)**：
   - `R1:Static-AST-Gate`（语法树静态硬拦截）
   - `R2:Metamorphic-Oracle`（蜕变关系与输入扰动）
   - `R3:Dynamic-Invariant-Contract`（运行时契约与霍尔三元组检验）
   - `R4:Closed-Loop-Critic`（多智能体批判自愈闭环）

---

## 🏛️ 经典问题论与学术病理学核心百科 (Master Pathology Catalog)

| 缺陷代码 | 经典学术命名 | 所属科学领域 | 权威经典出处 | 形式化本质与第一性成因 | 核心修复神谕 |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **PRB-E101** | **补丁过拟合 (Patch Overfitting)** | 软件工程学 (APR) | Smith et al. (FSE 2015), Le Goues (IEEE TSE) | 生成的代码仅硬编码特值使得现有测试集变绿，在任何未见过合法输入上失效。 | **蜕变测试神谕** (Metamorphic Invariant): 恒等单调性与全域参数扰动。 |
| **PRB-E102** | **规范投机 / 奖励作弊 (Specification Gaming)** | AI 对齐与安全 | DeepMind, OpenAI, Krakovna et al. (2020) | 智能体沿阻力最小路径优化，利用环境度量漏洞刷满分而架空真实意图。 | **沙箱不可变契约** (Immutable Sandboxed Invariants): 评测环境物理隔离。 |
| **PRB-E103** | **捷径学习 (Shortcut Learning)** | 机器学习与认知科学 | Geirhos et al. (Nature MI 2020) | 未学习真实因果律，仅拟合表面浅层线索，遇分布漂移（OOD）表现断崖式下跌。 | **对抗性输入扰动** (Adversarial Perturbation Oracle): 保持语义不变下的结构等价代换。 |
| **PRB-E104** | **同义反复验证 (Tautological Verification)** | 形式化验证与测试学 | Dijkstra, Parnas, Weyuker (1982) | 循环论证陷阱。断言与实现共享狭隘局部假设 ($A \implies A$)，直接抄被测公式作为期望。 | **双轨独立神谕** (Dual Independent Oracle): 强制断言源于正交独立基准模型。 |
| **PRB-E105** | **古德哈特定律失效 (Goodhart's Law)** | 控制论与社会技术系统 | Charles Goodhart (1975), Campbell (1979) | “当度量变成目标时便不再是好度量”。AI/人演化出无断言测试刷 100% 覆盖率的作弊路径。 | **变异测试与断言有效度** (Mutation Testing Gate): 变异算子注入杀死无断言假测试。 |
| **PRB-E106** | **聪明的汉斯效应 (Clever Hans Effect)** | 认知科学与模型评测 | Oskar Pfungst (1907), SWE-bench Audits | 格式极度美观但缺乏生产约束推理能力，遇并发重入或物理边界立即溃败。 | **混沌压力与对抗态验真** (Chaos Stress Testing Oracle): 在并发与故障注入中验真。 |
| **PRB-E107** | **螺旋幻觉死循环 (Spiraling Hallucination)** | 自主智能体架构 | SurgeHQ (2024), AutoGPT Autopsies | 首轮轻微捏造 API，后续轮次将其作为既成事实继续推导，层层污染导致认知雪崩。 | **单一真相源反射锚定** (Reflection Introspection Grounding): 强制调用真实运行时反射。 |
| **PRB-E108** | **静默吞异常与故障掩蔽 (Silent Error Swallow)** | 可靠性工程与防御编程 | CWE-391, Martin Fowler | 宽泛 `except Exception: pass` 吞没系统底层致命故障，破坏 Fail-Fast 原则。 | **静态 AST 裸异常拦截** (AST Bare-Except Guard): 拦截无日志与无处理的异常黑洞。 |
| **PRB-E109** | **抽象泄露与状态爆炸 (Leaky Abstraction)** | 系统架构与分布式计算 | Joel Spolsky (2002), C.A.R. Hoare | 假定底层网络/磁盘绝对完美，未处理物理世界真实时延与并发，触发隐式状态爆炸。 | **网络分区与幂等性事务** (Chaos Fault Injection & SAGA): 故障注入验证幂等性。 |
| **PRB-E110** | **伪造对象倒置 / Mock 作弊 (Mock Gaming)** | 软件测试工程学 | Martin Fowler (Mocks Aren't Stubs) | 过度 Mock 掉核心业务逻辑本身，导致测试演变为测试 Mock 库本身，实装即崩。 | **契约一致性测试** (Contract Verification): 限制 Mock 深度不超过 1 层，严禁 Mock 私有算子。 |

---

## ⚙️ 核心技术引擎与工程架构 (The 4 Pillars)

```
┌────────────────────────────────────────────────────────────────────────┐
│                        tool-problem-optima                             │
├───────────────────┬───────────────────┬────────────────────────────────┤
│ Pillar 1:         │ Pillar 2:         │ Pillar 3:                      │
│ AST Interceptor   │ MetamorphicOracle │ Supervisor Engine              │
│ (语法树刚性门禁)  │ (蜕变对抗神谕)    │ (闭环监督收敛状态机)           │
├───────────────────┴───────────────────┴────────────────────────────────┤
│ Pillar 4: Diagnostic Renderer (Miette/Rust 级高密度终端染色与张量雷达) │
└────────────────────────────────────────────────────────────────────────┘
```

### 1. AST Interceptor (语法树刚性门禁)
基于 Python 原生 AST 词法流，在代码执行前进行微秒级静态剖析：
- 精确拦截 `if x == 42 and y == 'foo': return 100` 等补丁过拟合特例分支；
- 拦截 `assert a == a`、`assert True` 等同义反复弱断言；
- 拦截测试函数中零断言的古德哈特定律刷量行为；
- 拦截 `except: pass` 裸异常吞噬。

### 2. Metamorphic Oracle (蜕变对抗神谕)
解决传统单元测试“点状采样不足”的绝症：
- **置换不变性 (Permutation Invariance)**：$f(x, y) == f(y, x)$；
- **幂等律不变式 (Idempotence)**：$f(f(x)) == f(x)$；
- **对抗性单调微扰**：对已通过测试用例施加结构等价扰动，瞬间击穿任何硬编码与捷径补丁。

### 3. Supervisor Engine (闭环监督收敛状态机)
为 AI 智能体与人类提供可验证的自愈状态流转：
$$\text{SUBMITTED} \to \text{AST\_AUDIT} \to \text{METAMORPHIC\_PROBING} \to \text{TENSOR\_DIVERGENCE} \to \text{CONVERGED\_VERIFIED}$$
如果代码存在缺陷，输出基于因果图的排错指引（Causal Remediation Guide），持续监督修复动作，直到缺陷总势能收敛至零。

### 4. Diagnostic Renderer (Miette 级终端诊断)
采用 ANSI 真彩色边框、精美源码高亮行、行内波浪指示器（`^^^^`）与 ASCII 张量雷达签名，输出顶级开发体验。

---

## 🏛️ 工业母机调用与技术选型溯源 (Mother-Machine Probing)

在本项目立项初期，严格调用宿主机工业母机装具进行技术选型：
1. **调用 `tool-stack-optima`**：
   - 执行指令：`python D:\github\tool-stack-optima\main.py run "基于第一性原理问题论、软件病理学与张量参数网络..."`
   - 得出结论：采用 **Pareto 最优单静态二进制/标准库自洽架构**，全核心无任何外部 pip 三方库依赖，启动内存小于 50MB，冷启动时延小于 10ms。
2. **调用 `tool-omniscout-radar`**：
   - 执行指令：`python D:\github\tool-omniscout-radar\main.py radar "AI automated program repair patch overfitting SWE-bench benchmark" --concise`
   - 对标吸收：`SWE-bench Verified`、`SpoonLabs/astor`、`iSEngLab/AwesomeLLM4APR`、`sola-st/RepairAgent`。

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

## 🛡️ 负向清单 (Non-Goals)

1. **坚决不引入庞大三方依赖**：100% 依托 Python 3.8+ 标准库实现，杜绝依赖地狱；
2. **坚决不做无因果解释的盲目报错**：任何报错必附学术领域、经典论文出处与蜕变修复神谕；
3. **坚决不做破坏性侵入修改**：审计引擎纯只读，通过状态机反例引导智能体收敛，而非越权硬改。

---

## 📜 许可证 (License)

本项目采用 [MIT License](LICENSE) 开源协议。
