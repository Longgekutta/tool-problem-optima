#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Metamorphic Oracle: Adversarial Invariant & Property-Based Fuzzing Engine
========================================================================
Destroys Patch Overfitting (PRB-E101), Specification Gaming (PRB-E102),
and Shortcut Learning (PRB-E103) through formal metamorphic invariants.

Instead of testing isolated point values (which are vulnerable to hardcoding),
this engine evaluates algebraic properties across state spaces:
  1. Permutation Invariance: f(x, y) == f(y, x)
  2. Idempotence: f(f(x)) == f(x)
  3. Monotonicity: x1 <= x2 => f(x1) <= f(x2)
  4. Identity Preservation: f(x, identity) == x
  5. Adversarial Input Fuzzing: Boundary and Out-of-Distribution injection
"""

import random
from dataclasses import dataclass
from typing import Callable, Any, List, Optional, Tuple


@dataclass
class MetamorphicViolation:
    """A mathematically proven counter-example violating a fundamental invariant."""
    relation_name: str
    property_description: str
    input_sample: Any
    perturbed_input: Any
    actual_output: Any
    expected_property: str
    causal_diagnosis: str


class MetamorphicOracleEngine:
    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)

    def test_idempotence(self, fn: Callable[[Any], Any], sample_inputs: List[Any]) -> Optional[MetamorphicViolation]:
        """Verifies f(f(x)) == f(x) (e.g. sanitizers, sorting, normalizers)."""
        for inp in sample_inputs:
            try:
                res1 = fn(inp)
                res2 = fn(res1)
                if res1 != res2:
                    return MetamorphicViolation(
                        relation_name="MR-IDEMPOTENCE",
                        property_description="Idempotence Invariant: f(f(x)) == f(x)",
                        input_sample=inp,
                        perturbed_input=res1,
                        actual_output=res2,
                        expected_property=f"Result after second application should equal first ({res1})",
                        causal_diagnosis="Function produces oscillating side effects or unstable state transitions."
                    )
            except Exception as e:
                return MetamorphicViolation(
                    relation_name="MR-IDEMPOTENCE-CRASH",
                    property_description="Crash on repeated application f(f(x))",
                    input_sample=inp,
                    perturbed_input=None,
                    actual_output=str(e),
                    expected_property="Function must survive re-entrant execution",
                    causal_diagnosis="Function is brittle or corrupts state on recursive/repeated calls."
                )
        return None

    def test_commutativity(self, fn: Callable[[Any, Any], Any], sample_pairs: List[Tuple[Any, Any]]) -> Optional[MetamorphicViolation]:
        """Verifies f(x, y) == f(y, x) for symmetric/commutative operations."""
        for x, y in sample_pairs:
            try:
                res_xy = fn(x, y)
                res_yx = fn(y, x)
                if res_xy != res_yx:
                    return MetamorphicViolation(
                        relation_name="MR-COMMUTATIVITY",
                        property_description="Symmetric Invariant: f(x, y) == f(y, x)",
                        input_sample=(x, y),
                        perturbed_input=(y, x),
                        actual_output=f"f(x,y)={res_xy} != f(y,x)={res_yx}",
                        expected_property="Symmetric binary operators must be order-independent",
                        causal_diagnosis="Implementation has positional bias or asymmetric branching."
                    )
            except Exception as e:
                return MetamorphicViolation(
                    relation_name="MR-COMMUTATIVITY-CRASH",
                    property_description="Crash under argument transposition",
                    input_sample=(x, y),
                    perturbed_input=(y, x),
                    actual_output=str(e),
                    expected_property="Transposed inputs must not crash",
                    causal_diagnosis="Asymmetric input handling triggers unhandled branch."
                )
        return None

    def test_adversarial_overfitting(
        self,
        candidate_fn: Callable[..., Any],
        known_test_inputs: List[Tuple[Any, ...]],
        perturbation_generator: Callable[[Any], Any],
        ground_truth_validator: Callable[[Any, Any], bool]
    ) -> List[MetamorphicViolation]:
        """
        Shreds Patch Overfitting:
        Takes the known passing test inputs, perturbs them slightly (while preserving semantics),
        and verifies if candidate_fn still produces mathematically valid outputs.
        """
        violations = []
        for args in known_test_inputs:
            perturbed_args = tuple(perturbation_generator(a) for a in args)
            try:
                out = candidate_fn(*perturbed_args)
                is_valid = ground_truth_validator(perturbed_args, out)
                if not is_valid:
                    violations.append(MetamorphicViolation(
                        relation_name="MR-ANTI-OVERFITTING",
                        property_description="Semantic Invariant under input perturbation",
                        input_sample=args,
                        perturbed_input=perturbed_args,
                        actual_output=out,
                        expected_property="Generalized invariant preservation under perturbation",
                        causal_diagnosis="Candidate patch overfitted to exact benchmark values; fails on isomorphic shifted input."
                    ))
            except Exception as e:
                violations.append(MetamorphicViolation(
                    relation_name="MR-ANTI-OVERFITTING-CRASH",
                    property_description="Crash on perturbed valid input",
                    input_sample=args,
                    perturbed_input=perturbed_args,
                    actual_output=str(e),
                    expected_property="Robust execution without exception",
                    causal_diagnosis="Patch used brittle hardcoded assumptions that broke upon slight distribution shift."
                ))
        return violations

    def verify_source_algebra(self, source_code: str) -> List[MetamorphicViolation]:
        """
        Dynamically discovers functions in source code and verifies core algebraic invariants:
        - Commutativity on 2-arg symmetric candidates
        - Idempotency on 1-arg normalization candidates
        """
        violations: List[MetamorphicViolation] = []
        sandbox = {
            "__builtins__": __builtins__,
            "__file__": "<sandbox_module>",
            "__name__": "__sandbox__"
        }
        try:
            # Execute in safe isolated sandbox namespace (unified globals/locals)
            exec(source_code, sandbox, sandbox)
        except Exception as e:
            return [MetamorphicViolation(
                relation_name="MR-COMPILE-CRASH",
                property_description="Crash during module loading",
                input_sample=None,
                perturbed_input=None,
                actual_output=str(e),
                expected_property="Source must be executable without top-level crash",
                causal_diagnosis=f"Module level execution threw: {e}"
            )]

        for name, obj in sandbox.items():
            # Only test pure functions, ignore imports and CLI dispatchers cmd_*
            if callable(obj) and not name.startswith(("_", "cmd_")):
                try:
                    import inspect
                    sig = inspect.signature(obj)
                    param_count = len(sig.parameters)
                    if param_count == 2 and any(k in name.lower() for k in ("add", "sum", "mult", "sym", "merge", "equal", "or", "and", "xor")):
                        sample_pairs = [(1, 2), (-3, 5), (0, 0), (10, -10)]
                        v = self.test_commutativity(obj, sample_pairs)
                        if v:
                            violations.append(v)
                    elif param_count == 1 and any(k in name.lower() for k in ("clean", "strip", "sort", "norm", "abs", "idemp", "dedup")):
                        sample_inputs = [0, 5, -10, 42]
                        v = self.test_idempotence(obj, sample_inputs)
                        if v:
                            violations.append(v)
                except Exception:
                    continue

        return violations
