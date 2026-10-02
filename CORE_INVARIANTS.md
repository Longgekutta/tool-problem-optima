# CORE_INVARIANTS.md: 计算问题论形式化不变式与适应度函数

> **项目规范**：`OMNI-PROJECT-SPEC Level 2` | `UCFS v1.0 Compliant` | `UTEO Rating: S-Master (Fixed-Point)`  
> **理论基础**：广义问题论 (General Problemology) + 认知病理学 (Cognitive Pathology) + 形式化验证 (Formal Methods)

---

## 🏛️ 第一性原理：问题本质的四维公理体系 (The 4-Space Axioms)

在计算学科中，一切错误（无论由人类神经元或人工神经网络生成）均非偶然的感性概念，而是以下四个空间之间的**非零散度张量 (Non-Zero Divergence Tensor)**：

$$\mathcal{P} \equiv \nabla(\mathcal{I}, \mathcal{S}, \mathcal{E}, \mathcal{C}) \neq \mathbf{0}$$

### 空间定义：
1. **$\mathcal{I}$ (Intent Space / 意图流形)**：系统的根本业务意图与真实物理因果律。
   $$\mathcal{I} = \{ u: \mathcal{W} \to \mathbb{R} \mid \text{满足全局效用最优化与业务不变式} \}$$
2. **$\mathcal{S}$ (Specification Space / 规范空间)**：外化的类型、前置条件、后置条件与测试集。
   $$\mathcal{S} = \{ (P, Q) \mid \{P\} C \{Q\} \}$$
3. **$\mathcal{E}$ (Execution Space / 实现与执行状态空间)**：语法树 AST、指令集与内存迁移轨迹。
   $$\mathcal{E} = \{ \sigma_0 \xrightarrow{\tau} \sigma_1 \xrightarrow{\tau} \dots \xrightarrow{\tau} \sigma_n \}$$
4. **$\mathcal{C}$ (Context Space / 环境与分布空间)**：输入分布、并发交错与边界资源约束。
   $$\mathcal{C} = \mathcal{D}_{\text{in}} \times \mathcal{T}_{\text{concurrency}} \times \mathcal{R}_{\text{limits}}$$

---

## 📐 五大基本散度流形 (The 5 Divergence Manifolds)

任何软件病理缺陷均可正交分解为以下五个基本分量：

| 散度符号 | 科学命名 | 数学定义 | 典型病理特例 |
| :--- | :--- | :--- | :--- |
| **$\Delta_{IS}$** | 目的论失配 (Teleological Gap) | $\lVert \mathcal{I} - \mathcal{S} \rVert$ | 规范投机 (Specification Gaming)、古德哈特定律失效 |
| **$\Delta_{SE}$** | 语义失调 (Semantic Gap) | $\lVert \mathcal{S} - \mathcal{E} \rVert$ | 逻辑崩溃、语法错误、空指针异常、状态机越界 |
| **$\Delta_{EC}$** | 环境失配 (Distributional Gap) | $\lVert \mathcal{E} - \mathcal{C} \rVert$ | 捷径学习 (Shortcut Learning)、竞态条件、内存泄漏 |
| **$\Delta_{VI}$** | 验证神谕假象 (Epistemic Illusion) | $\mathcal{V}(\mathcal{E}, \mathcal{S}) \to \text{True} \land \mathcal{E} \not\models \mathcal{I}$ | 补丁过拟合 (Patch Overfitting)、循环论证测试 |
| **$\Delta_{T}$** | 时空熵增漂移 (Temporal Decay) | $\frac{\partial \mathcal{E}}{\partial t} - \frac{\partial \mathcal{S}}{\partial t} > 0$ | 代码腐化、上下文漂移、隐式状态爆炸 |

---

## ⚡ 刚性架构适应度函数 (Rigid Fitness Functions)

本项目内置自动化适应度函数，确保治理引擎本身达到数学级自洽：

```python
def fitness_function_zero_defect_energy(report: AuditReport) -> bool:
    """Invariant 1: Total Defect Energy must converge to zero."""
    if report.tensor_divergence is None:
        return True
    return report.tensor_divergence.magnitude < 1e-4

def fitness_function_non_gaming_oracle(violation: Optional[MetamorphicViolation]) -> bool:
    """Invariant 2: Candidate implementation must be invariant-preserving under perturbation."""
    return violation is None

def fitness_function_fail_fast_soundness(findings: List[DiagnosticFinding]) -> bool:
    """Invariant 3: Zero unhandled bare except blocks (Fail-Fast Axiom)."""
    return not any(f.code == "PRB-E108" for f in findings)
```

---

## 🛡️ 负向清单 (Non-Goals)

根据 `OMNI-PROJECT-SPEC` 刚性约束，本项目明确界定以下非目标：
1. **不做重型外部依赖绑定**：坚决不引入庞大三方网络库或重量级模型运行时，核心引擎 100% 离线自洽于 Python 3.8+ 标准库；
2. **不做模糊无解释报错**：所有拦截必配学术领域、经典文献出处、数学第一性成因与蜕变修复神谕；
3. **不做破坏性越权文件写入**：审计模式定位纯只读无侵入，监督模式只提供形式化反例与收敛指导。
