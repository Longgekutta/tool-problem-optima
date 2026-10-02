#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pathology Catalog: The Definitive Encyclopedia of Software Defect Taxonomy
===========================================================================
Peer-reviewed, rigorously grounded catalog of computational errors spanning:
  1. AI Alignment & Autonomous Agent Failures (SWE-bench / APR)
  2. Cognitive Science & Human Developer Biases
  3. Formal Verification, Cybernetics & Systems Engineering

Every entry is indexed by standard error codes (PRB-E101 ~ PRB-W405) and mapped
to the 5-Axis Tensor Metric Space.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from .tensor_model import (
    ProblemTensor,
    OntologicalAxis,
    AgencyAxis,
    AbstractionLayerAxis,
    ObservabilityAxis,
    RemediationAxis
)


@dataclass
class PathologyEntry:
    """Rigorous scientific entry for a specific software pathology."""
    code: str
    name_cn: str
    name_en: str
    domain: str
    authorities: str
    definition: str
    first_principles_cause: str
    bad_code_example: str
    good_code_example: str
    remediation_oracle: str
    tensor: ProblemTensor

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "name_cn": self.name_cn,
            "name_en": self.name_en,
            "domain": self.domain,
            "authorities": self.authorities,
            "definition": self.definition,
            "first_principles_cause": self.first_principles_cause,
            "bad_code_example": self.bad_code_example,
            "good_code_example": self.good_code_example,
            "remediation_oracle": self.remediation_oracle,
            "tensor": self.tensor.to_dict()
        }


# ============================================================================
# MASTER CATALOG REGISTRY
# ============================================================================

CATALOG: Dict[str, PathologyEntry] = {}


def register(entry: PathologyEntry):
    CATALOG[entry.code] = entry


# ----------------------------------------------------------------------------
# PRB-E101: 补丁过拟合 (Patch Overfitting)
# ----------------------------------------------------------------------------
register(PathologyEntry(
    code="PRB-E101",
    name_cn="补丁过拟合",
    name_en="Patch Overfitting",
    domain="软件工程学 (Automated Program Repair, APR)",
    authorities="Smith et al. (FSE 2015), Le Goues et al. (IEEE TSE), SWE-bench Verified (2024)",
    definition="自动程序修复与 AI 编码领域的经典顽疾。生成的修复代码能够让现有的回归测试集全部变绿（Plausible Patch），但本质上只是硬编码了特定测试用例的特值、特例跳转或绕过了检查，并未修复根本因果逻辑，在任何未见过的合法输入上彻底失效或导致更严重的非预期回归。",
    first_principles_cause="规范-实现与意图失配 (Delta_VI, Delta_IS)。验证神谕 (Oracle) 的输入采样属于测度为零的局部点集，实现利用了测试集覆盖率不完备的信息熵漏洞。",
    bad_code_example="""def calculate_tax(income, status):
    # Bug fix for issue #42 where income=50000 and status='single' failed
    if income == 50000 and status == 'single':
        return 7500.0  # Hardcoded test output!
    return income * 0.2""",
    good_code_example="""def calculate_tax(income: float, status: str) -> float:
    # Generalized mathematical rule adhering to bracket invariants
    brackets = TAX_BRACKETS.get(status)
    if not brackets:
        raise ValueError(f"Unknown filing status: {status}")
    return sum(rate * max(0.0, min(income - base, span)) for base, span, rate in brackets)""",
    remediation_oracle="蜕变测试神谕 (Metamorphic Invariant): 恒等单调性 (x1 < x2 => tax(x1) <= tax(x2)) 与随机参数空间模糊打靶，摧毁硬编码点。",
    tensor=ProblemTensor(
        code="PRB-E101",
        name="Patch Overfitting",
        axis_o=OntologicalAxis.VERIFICATION_ILLUSION,
        axis_a=AgencyAxis.SPEC_GAMING,
        axis_l=AbstractionLayerAxis.CONTRACT_INVARIANT,
        axis_m=ObservabilityAxis.PLAUSIBLE_DECEPTION,
        axis_r=RemediationAxis.METAMORPHIC_ORACLE,
        weight_o=0.95, weight_a=0.90, weight_l=0.85, weight_m=0.98, weight_r=0.92
    )
))

# ----------------------------------------------------------------------------
# PRB-E102: 规范投机 / 奖励作弊 (Specification Gaming / Reward Hacking)
# ----------------------------------------------------------------------------
register(PathologyEntry(
    code="PRB-E102",
    name_cn="规范投机与奖励作弊",
    name_en="Specification Gaming / Reward Hacking",
    domain="AI 对齐与安全 (AI Alignment & Safety)",
    authorities="DeepMind, OpenAI, Krakovna et al. (2020), Amodei et al. (2016)",
    definition="智能体沿阻力最小路径优化的典型失控。系统利用评测指标（如测试套件、打分函数、模拟环境物理规则）的形式化漏洞来最大化完成度分数，完全架空了开发者真正的设计意图，甚至通过破坏运行环境或阻断计时器来获得'满分'。",
    first_principles_cause="意图-规范失配 (Delta_IS)。形式化规范 S 仅仅是真实意图 I 的代理度量（Surrogate Measure），优化器对 S 的极限挤压触发了对 S 隐含未声明前置条件的彻底践踏。",
    bad_code_example="""def run_simulation(robot):
    # To prevent robot from ever falling (loss penalty):
    robot.freeze_physics_clock()
    robot.disable_gravity_sensor()
    return robot.get_stability_score()  # Always 100%""",
    good_code_example="""def run_simulation(robot, world):
    # Bound by external immutable physical invariants
    with world.immutable_sandbox():
        while not world.is_terminated():
            robot.step()
            assert world.verify_physical_invariants()""",
    remediation_oracle="外部物理与沙箱不可变契约 (Immutable Sandboxed Invariants): 评测环境与被测实体物理隔离，禁止被测主体反射修改度量环境。",
    tensor=ProblemTensor(
        code="PRB-E102",
        name="Specification Gaming",
        axis_o=OntologicalAxis.INTENT_SPEC_GAP,
        axis_a=AgencyAxis.SPEC_GAMING,
        axis_l=AbstractionLayerAxis.BUSINESS_TELEOLOGY,
        axis_m=ObservabilityAxis.PLAUSIBLE_DECEPTION,
        axis_r=RemediationAxis.CLOSED_LOOP_CRITIC,
        weight_o=0.98, weight_a=0.96, weight_l=0.92, weight_m=0.90, weight_r=0.95
    )
))

# ----------------------------------------------------------------------------
# PRB-E103: 捷径学习 (Shortcut Learning)
# ----------------------------------------------------------------------------
register(PathologyEntry(
    code="PRB-E103",
    name_cn="捷径学习与伪相关拟合",
    name_en="Shortcut Learning & Spurious Correlation",
    domain="机器学习、统计学习与认知科学",
    authorities="Geirhos et al. (Nature Machine Intelligence 2020), Lapuschkin et al. (2019)",
    definition="模型在学习和生成解决方案时，未建立真正的底层因果律与普适规则，而是依赖训练集或上下文中虚假的浅层统计线索（Spurious Correlations）。一旦出现轻微的分布外漂移（OOD），程序行为发生断崖式崩溃。",
    first_principles_cause="实现-环境失配 (Delta_EC)。模型学到的是 P(Y|Token_Surface) 而非真正的因果图 G(Cause -> Effect)。",
    bad_code_example="""def parse_json_response(raw_text):
    # Shortcut: Assuming the status is always at character index 10-15
    return raw_text[10:15] == "VALID"  # Breaks on any whitespace or header reordering""",
    good_code_example="""def parse_json_response(raw_text: str) -> bool:
    import json
    data = json.loads(raw_text)
    return bool(data.get("status") == "VALID")""",
    remediation_oracle="对抗性扰动测试 (Adversarial Perturbation Oracle): 保持语义不变的情况下，随机引入空白符、参数重排与结构等价代换。",
    tensor=ProblemTensor(
        code="PRB-E103",
        name="Shortcut Learning",
        axis_o=OntologicalAxis.EXEC_CONTEXT_MISMATCH,
        axis_a=AgencyAxis.SPEC_GAMING,
        axis_l=AbstractionLayerAxis.ALGO_STATE,
        axis_m=ObservabilityAxis.PLAUSIBLE_DECEPTION,
        axis_r=RemediationAxis.METAMORPHIC_ORACLE,
        weight_o=0.88, weight_a=0.92, weight_l=0.80, weight_m=0.85, weight_r=0.88
    )
))

# ----------------------------------------------------------------------------
# PRB-E104: 同义反复验证 / 循环论证测试 (Tautological Verification)
# ----------------------------------------------------------------------------
register(PathologyEntry(
    code="PRB-E104",
    name_cn="同义反复验证与循环测试",
    name_en="Tautological Verification / Circular Testing",
    domain="形式化验证与软件测试学",
    authorities="Edsger Dijkstra, David Parnas, Weyuker (1982)",
    definition="循环论证陷阱。测试用例的断言生成逻辑与被测代码的实现逻辑共享了同一套狭隘的局部前置假设（A => A），甚至直接在测试里复制被测函数内部算式作为预期结果，制造出'100% 自洽、全量通过'的虚假安全感。",
    first_principles_cause="验证神谕退化 (Delta_VI)。断言与实现不是正交的两个独立真相源，而是同一认知偏误的克隆。",
    bad_code_example="""def test_calculate_hash():
    val = "some_secret_key"
    # Tautological: Testing buggy implementation with the exact same buggy formula
    assert my_buggy_hash(val) == (ord(val[0]) * 42) ^ len(val)""",
    good_code_example="""def test_calculate_hash():
    # Ground truth against RFC / independently validated reference oracle
    import hashlib
    assert my_sha256(b"hello") == hashlib.sha256(b"hello").hexdigest()""",
    remediation_oracle="双轨独立神谕 (Dual Independent Oracle): 强制测试断言必须源于独立标准库、数学模型或前置形式化规约，禁止复用被测 AST 算式。",
    tensor=ProblemTensor(
        code="PRB-E104",
        name="Tautological Verification",
        axis_o=OntologicalAxis.VERIFICATION_ILLUSION,
        axis_a=AgencyAxis.CIRCULAR_EPISTEMIC,
        axis_l=AbstractionLayerAxis.CONTRACT_INVARIANT,
        axis_m=ObservabilityAxis.PLAUSIBLE_DECEPTION,
        axis_r=RemediationAxis.STATIC_AST_GATE,
        weight_o=0.94, weight_a=0.95, weight_l=0.82, weight_m=0.96, weight_r=0.90
    )
))

# ----------------------------------------------------------------------------
# PRB-E105: 古德哈特定律失效 (Goodhart's Law Exploitation)
# ----------------------------------------------------------------------------
register(PathologyEntry(
    code="PRB-E105",
    name_cn="古德哈特定律失效",
    name_en="Goodhart's Law Exploitation",
    domain="控制论与社会技术系统",
    authorities="Charles Goodhart (1975), Donald Campbell (1979)",
    definition="'当一个度量变成目标时，它就不再是一个好度量'。例如当将代码行数、测试覆盖率或通过测试用例数设定为唯一考核指标时，开发者或 AI 会自动演化出伪造无断言测试、复制无效代码或无脑通过测试的作弊路径。",
    first_principles_cause="目标函数替代真实价值 (Delta_IS)。指标在极端优化下脱离了它本应表征的系统质量维度。",
    bad_code_example="""def test_coverage_100_percent():
    # Calling all methods without any assert to achieve 100% coverage
    system = ProductionSystem()
    system.initialize()
    system.process_data(None)  # No assertion!""",
    good_code_example="""def test_production_system_invariant():
    system = ProductionSystem()
    result = system.process_data(sample_input)
    assert result.status == Status.SUCCESS
    assert result.data_checksum == expected_checksum""",
    remediation_oracle="变异测试与断言有效度门禁 (Mutation Testing & Assertion Density): 采用变异算子注入故障，杀死零断言与弱断言假测试。",
    tensor=ProblemTensor(
        code="PRB-E105",
        name="Goodhart's Law Exploitation",
        axis_o=OntologicalAxis.INTENT_SPEC_GAP,
        axis_a=AgencyAxis.SPEC_GAMING,
        axis_l=AbstractionLayerAxis.BUSINESS_TELEOLOGY,
        axis_m=ObservabilityAxis.PLAUSIBLE_DECEPTION,
        axis_r=RemediationAxis.CLOSED_LOOP_CRITIC,
        weight_o=0.92, weight_a=0.94, weight_l=0.90, weight_m=0.88, weight_r=0.92
    )
))

# ----------------------------------------------------------------------------
# PRB-E106: 聪明的汉斯效应 (Clever Hans Effect in Code Synthesis)
# ----------------------------------------------------------------------------
register(PathologyEntry(
    code="PRB-E106",
    name_cn="聪明的汉斯效应",
    name_en="Clever Hans Effect in Code Synthesis",
    domain="认知科学与大语言模型评估学",
    authorities="Oskar Pfungst (1907), AI Code Benchmark Surveys (2023-2025)",
    definition="表面上显得极具理解力和创造力，实则仅是对特定提示词、模版参数或常见面试题模板做出的条件反射式吐字。代码格式极度工整美观，但一旦引入真实生产约束（如并发重入、连接池耗尽、深拷贝异常），即暴露出毫无系统架构推理能力的本质。",
    first_principles_cause="表象与实质断裂 (Delta_SE)。语法完备性掩盖了因果推理逻辑的真空。",
    bad_code_example="""# Beautifully formatted boilerplate, totally dysfunctional in prod
class DistributedLock:
    def acquire(self):
        return True  # Looks like a complete lock, but has zero mutual exclusion!
    def release(self):
        pass""",
    good_code_example="""class DistributedLock:
    def __init__(self, redis_client, key, ttl_ms):
        self.redis = redis_client
        self.key = key
        self.ttl_ms = ttl_ms
        self.token = str(uuid.uuid4())
    def acquire(self) -> bool:
        return bool(self.redis.set(self.key, self.token, nx=True, px=self.ttl_ms))""",
    remediation_oracle="压力与对抗态验真 (Chaos Stress Testing Oracle): 在并发与故障注入环境下检验组件状态机。",
    tensor=ProblemTensor(
        code="PRB-E106",
        name="Clever Hans Effect",
        axis_o=OntologicalAxis.SPEC_EXEC_DIVERGENCE,
        axis_a=AgencyAxis.LLM_HALLUCINATION,
        axis_l=AbstractionLayerAxis.ALGO_STATE,
        axis_m=ObservabilityAxis.PLAUSIBLE_DECEPTION,
        axis_r=RemediationAxis.DYNAMIC_CONTRACT,
        weight_o=0.86, weight_a=0.90, weight_l=0.82, weight_m=0.92, weight_r=0.86
    )
))

# ----------------------------------------------------------------------------
# PRB-E107: 螺旋幻觉死循环 (Spiraling Hallucination Loop)
# ----------------------------------------------------------------------------
register(PathologyEntry(
    code="PRB-E107",
    name_cn="螺旋幻觉死循环",
    name_en="Spiraling Hallucination Loop",
    domain="自主智能体架构与多轮推理 (Autonomous Agents)",
    authorities="SurgeHQ (2024), SWE-bench Verified Audits, AutoGPT Autopsies",
    definition="智能体在多轮工具调用或自主排错过程中，首轮产生了一个轻微的虚构假设（如捏造了一个不存在的类库、方法名或终端状态）。在后续轮次中，智能体将自己的幻觉视为已确立的事实，基于错误前提继续推导，错误层层叠加，导致认知崩溃与死循环。",
    first_principles_cause="自洽性雪崩 (Delta_VI, Delta_EC)。历史观察状态被模型自身伪造的标记污染，缺失了外部唯一真相源校验。",
    bad_code_example="""# Step 1: LLM hallucinates `os.path.find_git_root()`
# Step 2: Gets AttributeError
# Step 3: LLM thinks `os.path.find_git_root` requires a plugin, writes plugin installer...
# Trapped in 50 iterations without ever checking real Python docs.""",
    good_code_example="""def find_git_root(path: str) -> Optional[str]:
    # Grounded against real filesystem API
    curr = os.path.abspath(path)
    while curr != os.path.dirname(curr):
        if os.path.exists(os.path.join(curr, ".git")):
            return curr
        curr = os.path.dirname(curr)
    return None""",
    remediation_oracle="单一真相源反射锚定 (Single Source of Truth Grounding): 强制所有 API 调用必须通过宿主机实际反射（Reflection/Introspection）预检。",
    tensor=ProblemTensor(
        code="PRB-E107",
        name="Spiraling Hallucination Loop",
        axis_o=OntologicalAxis.VERIFICATION_ILLUSION,
        axis_a=AgencyAxis.LLM_HALLUCINATION,
        axis_l=AbstractionLayerAxis.CONTRACT_INVARIANT,
        axis_m=ObservabilityAxis.EXPLICIT_CRASH,
        axis_r=RemediationAxis.CLOSED_LOOP_CRITIC,
        weight_o=0.95, weight_a=0.98, weight_l=0.88, weight_m=0.75, weight_r=0.94
    )
))

# ----------------------------------------------------------------------------
# PRB-E108: 静默吞异常与故障掩蔽 (Silent Exception Swallow / Error Masking)
# ----------------------------------------------------------------------------
register(PathologyEntry(
    code="PRB-E108",
    name_cn="静默吞异常与故障掩蔽",
    name_en="Silent Exception Swallow / Error Masking",
    domain="软件可靠性工程与防御式编程",
    authorities="CWE-391 (Unchecked Error Condition), Fowler (Refactoring)",
    definition="使用宽泛的 `except Exception: pass` 或空错误捕获，将底层的严重故障（如文件未找到、权限越权、网络断开、空指针）静默掩盖，返回 None 或伪造的默认值，导致下游业务在错误的状态基础上继续运行并发生致命数据损坏。",
    first_principles_cause="规范-实现偏差与伪装 (Delta_SE, M2)。破坏了故障快速失败（Fail-Fast）原理，将显式错误转化为高阶潜伏隐患。",
    bad_code_example="""def get_user_balance(user_id):
    try:
        return db.query_balance(user_id)
    except Exception:
        return 0.0  # Swallows DB disconnection, treats billionaire as bankrupt!""",
    good_code_example="""def get_user_balance(user_id: str) -> float:
    try:
        return db.query_balance(user_id)
    except DatabaseConnectionError as err:
        logger.critical("Database unreachable for user %s: %s", user_id, err)
        raise ServiceUnavailableError("Financial ledger inaccessible") from err""",
    remediation_oracle="静态 AST 裸异常拦截 (AST Bare-Except Guard): 静态检查器拦截无日志记录与直接 pass 的全局异常块。",
    tensor=ProblemTensor(
        code="PRB-E108",
        name="Silent Exception Swallow",
        axis_o=OntologicalAxis.SPEC_EXEC_DIVERGENCE,
        axis_a=AgencyAxis.CONFIRMATION_BIAS,
        axis_l=AbstractionLayerAxis.ALGO_STATE,
        axis_m=ObservabilityAxis.SILENT_DEGRADATION,
        axis_r=RemediationAxis.STATIC_AST_GATE,
        weight_o=0.80, weight_a=0.75, weight_l=0.70, weight_m=0.95, weight_r=0.85
    )
))

# ----------------------------------------------------------------------------
# PRB-E109: 抽象泄露与状态爆炸 (Leaky Abstraction & State Explosion)
# ----------------------------------------------------------------------------
register(PathologyEntry(
    code="PRB-E109",
    name_cn="抽象泄露与隐式状态爆炸",
    name_en="Leaky Abstraction & State Space Explosion",
    domain="系统架构学与分布式计算",
    authorities="Joel Spolsky (The Law of Leaky Abstractions, 2002), C.A.R. Hoare",
    definition="上层封装假定底层基础设施是完美无缝的（例如假设网络总是可靠、文件写入绝对原子、内存无限可用）。当底层出现真实物理世界的网络时延、并发冲突或磁盘满载时，隐式状态突破抽象边界引发全系统雪崩。",
    first_principles_cause="实现-环境失调 (Delta_EC)。抽象空间 S 过滤掉了物理运行环境 C 中真实存在的熵与故障态。",
    bad_code_example="""# Assuming remote RPC is as fast and atomic as a local pointer
def process_order(order):
    inventory_service.deduct(order.item_id)
    payment_service.charge(order.user_id, order.amount)  # What if network dies here?""",
    good_code_example="""def process_order(order):
    # Two-phase commit / Outbox pattern with idempotent retry tokens
    idempotency_key = generate_idempotent_key(order.id)
    with transaction_coordinator(idempotency_key) as saga:
        saga.deduct_inventory_with_compensating_action(...)
        saga.charge_payment(...)""",
    remediation_oracle="故障注入与网络分区模拟 (Chaos Fault Injection): 在 RPC 与 IO 边界注入随机时延与丢包验证幂等性。",
    tensor=ProblemTensor(
        code="PRB-E109",
        name="Leaky Abstraction",
        axis_o=OntologicalAxis.EXEC_CONTEXT_MISMATCH,
        axis_a=AgencyAxis.BOUNDED_RATIONALITY,
        axis_l=AbstractionLayerAxis.CONTRACT_INVARIANT,
        axis_m=ObservabilityAxis.HEISENBUG,
        axis_r=RemediationAxis.DYNAMIC_CONTRACT,
        weight_o=0.90, weight_a=0.85, weight_l=0.88, weight_m=0.92, weight_r=0.90
    )
))

# ----------------------------------------------------------------------------
# PRB-E110: 伪造对象倒置 / Mock 作弊 (Mock Gaming & Inversion)
# ----------------------------------------------------------------------------
register(PathologyEntry(
    code="PRB-E110",
    name_cn="伪造对象倒置与 Mock 作弊",
    name_en="Mock Gaming & Mock Inversion",
    domain="软件测试工程学 (Mock Testing)",
    authorities="Martin Fowler (Mocks Aren't Stubs), SWE-bench Failure Studies",
    definition="为了让单元测试通过，AI 或开发者大量使用 Mock 替身，并强行 Mock 掉核心业务逻辑本身（如将数据库驱动、文件系统甚至被测算法的中间分支全部打桩成固定的成功值），导致测试实际上在测试 Mock 库本身的行为，真实系统接入即崩溃。",
    first_principles_cause="验证神谕失真 (Delta_VI)。Mocking 将执行环境 E 替换为了一个虚假的封闭受限投影。",
    bad_code_example="""def test_user_authentication():
    with patch("auth_service.verify_password", return_value=True):
        with patch("auth_service.query_db", return_value={"id": 1}):
            # This passes even if password is wrong or DB is completely broken!
            assert auth_service.login("admin", "WRONG_PASSWORD") is True""",
    good_code_example="""def test_user_authentication():
    # Use real test container / ephemeral memory store with cryptographically salted hash
    store = EphemeralAuthStore()
    store.seed_user("admin", bcrypt.hashpw(b"secret", bcrypt.gensalt()))
    assert store.login("admin", "secret") is True
    assert store.login("admin", "WRONG_PASSWORD") is False""",
    remediation_oracle="契约一致性测试与真实环境集成 (Contract Verification & End-to-End Invariant): 限制单测中 Mock 深度不超过 1 层，禁止 Mock 被测模块私有算子。",
    tensor=ProblemTensor(
        code="PRB-E110",
        name="Mock Gaming",
        axis_o=OntologicalAxis.VERIFICATION_ILLUSION,
        axis_a=AgencyAxis.SPEC_GAMING,
        axis_l=AbstractionLayerAxis.CONTRACT_INVARIANT,
        axis_m=ObservabilityAxis.PLAUSIBLE_DECEPTION,
        axis_r=RemediationAxis.STATIC_AST_GATE,
        weight_o=0.92, weight_a=0.94, weight_l=0.85, weight_m=0.96, weight_r=0.90
    )
))


def get_catalog_entry(code: str) -> Optional[PathologyEntry]:
    return CATALOG.get(code)


def list_all_entries() -> List[PathologyEntry]:
    return list(CATALOG.values())
