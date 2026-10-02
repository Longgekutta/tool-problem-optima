#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tensor Parameter Network: 5-Axis Orthogonal Coordinate Space
============================================================
Translates any software problem (AI-generated or human-written) into a
rigorous 5-dimensional tensor embedding:
  Axis O: Ontological Origin (本体根源)
  Axis A: Agency & Cognitive Failure Mode (主体认知机制)
  Axis L: Epistemic Abstraction Layer (知识能级)
  Axis M: Observability & Masking Depth (可观测性与伪装层深)
  Axis R: Remediation Dynamics (修复动力学与闭环收敛)
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Any
import math


class OntologicalAxis(Enum):
    """Axis O: The ontological origin of the defect."""
    INTENT_SPEC_GAP = "O1:Intent-Spec-Gap"               # 意图-规范失配
    SPEC_EXEC_DIVERGENCE = "O2:Spec-Exec-Divergence"     # 规范-实现偏差
    EXEC_CONTEXT_MISMATCH = "O3:Exec-Context-Mismatch"   # 实现-环境失调
    VERIFICATION_ILLUSION = "O4:Verification-Illusion"   # 验证神谕假象
    TEMPORAL_ENTROPY = "O5:Temporal-Entropy"             # 演化与认知衰退


class AgencyAxis(Enum):
    """Axis A: The cognitive / agentic failure mechanism."""
    LLM_HALLUCINATION = "A1:Statistical-Hallucination"   # 统计型虚构
    SPEC_GAMING = "A2:Optimization-Gaming"               # 目标投机与捷径
    BOUNDED_RATIONALITY = "A3:Bounded-Rationality"       # 有限理性与过载
    CONFIRMATION_BIAS = "A4:Confirmation-Bias"           # 确认偏误与盲区
    CIRCULAR_EPISTEMIC = "A5:Circular-Epistemic"         # 同义反复与循环自洽


class AbstractionLayerAxis(Enum):
    """Axis L: The abstraction depth where the defect manifests."""
    SYNTACTIC = "L1:Syntactic-Lexical"                   # 句法与词法级
    TYPE_MEMORY = "L2:Type-Memory-Safety"                # 类型与内存边界级
    ALGO_STATE = "L3:Algorithm-State"                    # 算法与状态迁移级
    CONTRACT_INVARIANT = "L4:Contract-Invariant"         # 契约与不变式级
    BUSINESS_TELEOLOGY = "L5:Business-Teleology"         # 业务意图与系统目标级


class ObservabilityAxis(Enum):
    """Axis M: How the defect presents itself to oracles and humans."""
    EXPLICIT_CRASH = "M1:Explicit-Crash"                 # 立即暴露崩溃
    SILENT_DEGRADATION = "M2:Silent-Degradation"         # 静默腐化/泄漏
    PLAUSIBLE_DECEPTION = "M3:Plausible-Green-Deception" # 伪绿假象 (通过现有测试)
    HEISENBUG = "M4:Intermittent-Heisenbug"              # 测不准/偶发竞态


class RemediationAxis(Enum):
    """Axis R: The minimal control mechanism required for eradication."""
    STATIC_AST_GATE = "R1:Static-AST-Gate"               # 语法树静态硬拦截
    METAMORPHIC_ORACLE = "R2:Metamorphic-Oracle"         # 蜕变关系与输入扰动
    DYNAMIC_CONTRACT = "R3:Dynamic-Invariant-Contract"   # 运行时霍尔三元组检验
    CLOSED_LOOP_CRITIC = "R4:Closed-Loop-Critic"         # 多智能体批判自愈闭环


@dataclass
class ProblemTensor:
    """
    Formal 5-Axis Tensor point in Problem Space.
    """
    code: str                                # Unique Code e.g. PRB-E101
    name: str                                # Scientific name
    axis_o: OntologicalAxis
    axis_a: AgencyAxis
    axis_l: AbstractionLayerAxis
    axis_m: ObservabilityAxis
    axis_r: RemediationAxis
    
    # Quantitative weights [0.0 - 1.0] along the 5 axes
    weight_o: float = 0.8
    weight_a: float = 0.8
    weight_l: float = 0.8
    weight_m: float = 0.9
    weight_r: float = 0.9

    @property
    def vector(self) -> List[float]:
        """Normalized 5-dimensional coordinate vector."""
        return [self.weight_o, self.weight_a, self.weight_l, self.weight_m, self.weight_r]

    def distance_to(self, other: "ProblemTensor") -> float:
        """Euclidean metric distance in tensor space."""
        v1 = self.vector
        v2 = other.vector
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

    def render_ascii_radar(self) -> str:
        """Renders a compact ASCII radar signature."""
        def bar(val: float, length: int = 10) -> str:
            filled = int(round(val * length))
            return "■" * filled + "□" * (length - filled)

        lines = [
            f"┌── [Tensor Signature: {self.code}] ──────────────────────────────┐",
            f"│  Ontological (O) : {bar(self.weight_o)} {self.weight_o:.2f} [{self.axis_o.value.split(':')[1]}]",
            f"│  Agency Mode (A) : {bar(self.weight_a)} {self.weight_a:.2f} [{self.axis_a.value.split(':')[1]}]",
            f"│  Layer Depth (L) : {bar(self.weight_l)} {self.weight_l:.2f} [{self.axis_l.value.split(':')[1]}]",
            f"│  Masking Lvl (M) : {bar(self.weight_m)} {self.weight_m:.2f} [{self.axis_m.value.split(':')[1]}]",
            f"│  Remediation (R) : {bar(self.weight_r)} {self.weight_r:.2f} [{self.axis_r.value.split(':')[1]}]",
            f"└──────────────────────────────────────────────────────────────────┘"
        ]
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "name": self.name,
            "axes": {
                "ontological": self.axis_o.value,
                "agency": self.axis_a.value,
                "layer": self.axis_l.value,
                "observability": self.axis_m.value,
                "remediation": self.axis_r.value,
            },
            "weights": {
                "o": self.weight_o,
                "a": self.weight_a,
                "l": self.weight_l,
                "m": self.weight_m,
                "r": self.weight_r,
            }
        }
