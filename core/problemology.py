#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core Problemology: Computational Problem Theory & Epistemic Divergence Tensor
=============================================================================
First-principles mathematical formulation of problems in software engineering.

A problem (or defect) is NOT merely an AI flaw or human mistake. Fundamentally,
any computational problem is a non-zero divergence tensor between four primitive spaces:
  1. I (Intent Space / 意图流形): Latent invariant utility & teleological goals.
  2. S (Specification Space / 规范空间): Explicit formal assertions, types & contracts.
  3. E (Execution Space / 实现与执行状态空间): Concrete AST, bytecode & state trajectories.
  4. C (Context Space / 环境与分布空间): Operating conditions, concurrency & domain inputs.

Universal Defect Invariant:
  Problem = DivergenceTensor(I, S, E, C) != 0
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
import math


class FundamentalSpace(Enum):
    """The four primitive spaces of Computational Problemology."""
    INTENT = "I"           # 意图空间 (Teleological Intent & Latent Invariants)
    SPECIFICATION = "S"    # 规范空间 (Formal Contracts, Types, Assertions)
    EXECUTION = "E"        # 执行空间 (AST, Machine Instructions, Memory States)
    CONTEXT = "C"          # 环境空间 (Runtime, Concurrency, Input Distributions)


class DivergenceType(Enum):
    """Taxonomy of First-Principles Space Divergences."""
    TELEOLOGICAL = "I_S_GAP"       # Intent-Specification Mismatch (Gaming, Goodhart)
    SEMANTIC = "S_E_GAP"           # Specification-Execution Divergence (Bugs, Crashes)
    DISTRIBUTIONAL = "E_C_GAP"     # Execution-Context Incompatibility (Shortcut, Leaks)
    EPISTEMIC = "VERIFICATION_ILLUSION" # Oracle Inadequacy (Patch Overfitting, Circular Tests)
    TEMPORAL = "ENTROPY_DRIFT"     # Drift over time / cognitive decay


@dataclass
class SpaceCoordinates:
    """Coordinate representation in the 4-space manifold."""
    intent_fidelity: float = 1.0       # [0.0, 1.0] Alignment with true business invariant
    spec_coverage: float = 1.0         # [0.0, 1.0] Completeness of formal specifications
    exec_soundness: float = 1.0        # [0.0, 1.0] Soundness of execution state transitions
    context_resilience: float = 1.0    # [0.0, 1.0] Robustness under distribution shifts & concurrency

    def is_ideal(self, epsilon: float = 1e-4) -> bool:
        """Determines if the system state is invariant-preserving (zero defect)."""
        return (
            abs(self.intent_fidelity - 1.0) < epsilon and
            abs(self.spec_coverage - 1.0) < epsilon and
            abs(self.exec_soundness - 1.0) < epsilon and
            abs(self.context_resilience - 1.0) < epsilon
        )


@dataclass
class ProblemDivergenceTensor:
    """
    Multi-dimensional divergence tensor quantifying the gap between (I, S, E, C).
    
    T = [Delta_IS, Delta_SE, Delta_EC, Delta_VI, Delta_Time]
    """
    delta_is: float  # Teleological gap: Specification gaming / Goodhart metric
    delta_se: float  # Semantic gap: Logic bugs, crashes, type mismatches
    delta_ec: float  # Contextual gap: Shortcut learning, OOD brittleness, race conditions
    delta_vi: float  # Epistemic gap: Patch overfitting, circular/tautological test validation
    delta_t: float   # Temporal decay: Code rot, technical debt, forgotten context

    @property
    def magnitude(self) -> float:
        """Frobenius norm of the divergence tensor (Total Defect Energy)."""
        return math.sqrt(
            self.delta_is ** 2 +
            self.delta_se ** 2 +
            self.delta_ec ** 2 +
            self.delta_vi ** 2 +
            self.delta_t ** 2
        )

    @property
    def primary_divergence(self) -> DivergenceType:
        """Identifies the dominant failure manifold."""
        gaps = {
            DivergenceType.TELEOLOGICAL: self.delta_is,
            DivergenceType.SEMANTIC: self.delta_se,
            DivergenceType.DISTRIBUTIONAL: self.delta_ec,
            DivergenceType.EPISTEMIC: self.delta_vi,
            DivergenceType.TEMPORAL: self.delta_t,
        }
        return max(gaps, key=gaps.get)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "magnitude": round(self.magnitude, 4),
            "primary_divergence": self.primary_divergence.value,
            "components": {
                "delta_is_teleological": round(self.delta_is, 4),
                "delta_se_semantic": round(self.delta_se, 4),
                "delta_ec_distributional": round(self.delta_ec, 4),
                "delta_vi_epistemic": round(self.delta_vi, 4),
                "delta_t_temporal": round(self.delta_t, 4),
            }
        }


def compute_tensor_divergence(coords: SpaceCoordinates) -> ProblemDivergenceTensor:
    """Computes the first-principles divergence tensor from space coordinates."""
    # Delta_IS: when intent is high but spec is loose, or spec is gamed
    delta_is = max(0.0, coords.intent_fidelity - coords.spec_coverage)
    
    # Delta_SE: when spec exists but execution violates it
    delta_se = max(0.0, coords.spec_coverage - coords.exec_soundness)
    
    # Delta_EC: execution cannot handle contextual variance
    delta_ec = max(0.0, coords.exec_soundness - coords.context_resilience)
    
    # Delta_VI: execution appears sound according to weak spec, but violates true intent
    # Classic patch overfitting metric: High exec pass rate on weak spec, low intent fidelity
    delta_vi = max(0.0, coords.exec_soundness * (1.0 - coords.intent_fidelity))
    
    # Delta_T: entropy factor
    delta_t = 0.5 * (delta_is + delta_ec)

    return ProblemDivergenceTensor(
        delta_is=delta_is,
        delta_se=delta_se,
        delta_ec=delta_ec,
        delta_vi=delta_vi,
        delta_t=delta_t
    )
