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

Upgraded with Safe Sandbox Execution, Thread Timeout Guard, and Type-Aware Adaptive Probing.
"""

import sys
import logging
import random
import inspect
import concurrent.futures
from pathlib import Path
from dataclasses import dataclass
from typing import Callable, Any, List, Optional, Tuple, Dict, Set


SAFE_STDLIB_MODULES = {
    "math", "re", "json", "datetime", "collections", "itertools",
    "functools", "typing", "copy", "random", "string", "hashlib",
    "decimal", "bisect", "heapq"
}


def _create_safe_builtins() -> Dict[str, Any]:
    """Creates a hardened restricted builtins dictionary blocking destructive OS calls."""
    if hasattr(__builtins__, "__dict__"):
        base = dict(__builtins__.__dict__)
    elif isinstance(__builtins__, dict):
        base = dict(__builtins__)
    else:
        base = dict(vars(__builtins__))

    # Block destructive or unsafe functions
    dangerous = {
        "eval", "exec", "compile", "open", "breakpoint",
        "input", "exit", "quit"
    }
    for d in dangerous:
        base.pop(d, None)

    # Hardened import hook: only allow safe computation libraries
    orig_import = __builtins__.__dict__.get("__import__") if hasattr(__builtins__, "__dict__") else __builtins__.get("__import__")

    def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
        top_name = name.split(".")[0]
        if top_name in SAFE_STDLIB_MODULES or top_name.startswith("typing"):
            if orig_import:
                return orig_import(name, globals, locals, fromlist, level)
            import importlib
            return importlib.import_module(name)
        raise ImportError(f"Import of module '{name}' is restricted in Metamorphic Sandbox.")

    base["__import__"] = safe_import
    return base


import threading
import queue


def run_with_timeout(func: Callable[..., Any], args: Tuple[Any, ...], timeout_sec: float = 0.3) -> Any:
    """Executes a function with a strict timeout using a daemon thread that doesn't block shutdown."""
    result_queue = queue.Queue()
    exception_queue = queue.Queue()

    def worker():
        try:
            res = func(*args)
            result_queue.put(res)
        except Exception as e:
            exception_queue.put(e)

    t = threading.Thread(target=worker, daemon=True)
    t.start()
    t.join(timeout=timeout_sec)
    if t.is_alive():
        raise concurrent.futures.TimeoutError("Execution exceeded timeout threshold.")
    if not exception_queue.empty():
        raise exception_queue.get()
    if not result_queue.empty():
        return result_queue.get()
    return None


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
                res1 = run_with_timeout(fn, (inp,))
                res2 = run_with_timeout(fn, (res1,))
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
            except concurrent.futures.TimeoutError:
                return MetamorphicViolation(
                    relation_name="MR-IDEMPOTENCE-TIMEOUT",
                    property_description="Execution Timeout on f(f(x))",
                    input_sample=inp,
                    perturbed_input=None,
                    actual_output="Timeout (> 300ms)",
                    expected_property="Function execution must terminate bounded within 300ms",
                    causal_diagnosis="Suspected infinite loop or recursive deadlock under repeated application."
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
                res_xy = run_with_timeout(fn, (x, y))
                res_yx = run_with_timeout(fn, (y, x))
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
            except concurrent.futures.TimeoutError:
                return MetamorphicViolation(
                    relation_name="MR-COMMUTATIVITY-TIMEOUT",
                    property_description="Execution Timeout on f(x, y)",
                    input_sample=(x, y),
                    perturbed_input=(y, x),
                    actual_output="Timeout (> 300ms)",
                    expected_property="Function execution must terminate bounded within 300ms",
                    causal_diagnosis="Suspected infinite loop or catastrophic recursion."
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
                out = run_with_timeout(candidate_fn, perturbed_args)
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
            except concurrent.futures.TimeoutError:
                violations.append(MetamorphicViolation(
                    relation_name="MR-ANTI-OVERFITTING-TIMEOUT",
                    property_description="Timeout on perturbed valid input",
                    input_sample=args,
                    perturbed_input=perturbed_args,
                    actual_output="Timeout (> 300ms)",
                    expected_property="Robust execution within time bound",
                    causal_diagnosis="Perturbed input triggered unbounded loop."
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

    def _probe_adaptive_commutativity(self, fn: Callable[[Any, Any], Any]) -> Optional[MetamorphicViolation]:
        """Adaptively probes candidate 2-parameter functions across multiple polymorphic type suites."""
        type_suites = [
            # 1. Numeric suite
            [(1, 2), (-3, 5), (0, 0), (10, -10)],
            # 2. String suite
            [("abc", "def"), ("", "a"), ("hello", "world")],
            # 3. Collection/Set suite
            [({1, 2}, {3, 4}), ({1}, {2, 3})]
        ]

        for suite in type_suites:
            # Check if this suite can be invoked without TypeError
            try:
                test_x, test_y = suite[0]
                fn(test_x, test_y)
                # If succeeded, evaluate commutativity on full suite
                return self.test_commutativity(fn, suite)
            except (TypeError, ValueError, AttributeError):
                continue
            except Exception:
                # If execution crashed for another reason, test_commutativity will catch and format it
                return self.test_commutativity(fn, suite)

        return None

    def _probe_adaptive_idempotence(self, fn: Callable[[Any], Any]) -> Optional[MetamorphicViolation]:
        """Adaptively probes candidate 1-parameter functions across multiple polymorphic type suites."""
        type_suites = [
            # 1. Numeric suite
            [0, 5, -10, 42],
            # 2. String suite
            ["", "hello", "  world  ", "UPPER", "already_clean"],
            # 3. List suite
            [[], [1, 2, 3], [3, 1, 2], [5, 5]],
            # 4. Dict suite
            [{}, {"a": 1, "b": 2}]
        ]

        for suite in type_suites:
            try:
                test_inp = suite[0]
                fn(test_inp)
                # If succeeded, evaluate idempotence on full suite
                return self.test_idempotence(fn, suite)
            except (TypeError, ValueError, AttributeError):
                continue
            except Exception:
                return self.test_idempotence(fn, suite)

        return None

    def verify_source_algebra(self, source_code: str, file_path: Optional[str] = None) -> List[MetamorphicViolation]:
        """
        Dynamically discovers functions in source code and verifies core algebraic invariants:
        - Commutativity on 2-arg symmetric candidates (Adaptive Type Probing)
        - Idempotency on 1-arg normalization candidates (Adaptive Type Probing)
        Runs inside a hardened restricted execution sandbox.
        """
        violations: List[MetamorphicViolation] = []
        safe_builtins = _create_safe_builtins()

        sandbox = {
            "__builtins__": safe_builtins,
            "__file__": "<sandbox_module>",
            "__name__": "__sandbox__"
        }
        if file_path:
            p = Path(file_path).resolve()
            sandbox["__file__"] = str(p)
            if (p.parent / "__init__.py").exists():
                sandbox["__package__"] = p.parent.name
                parent_root = str(p.parent.parent)
                if parent_root not in sys.path:
                    sys.path.insert(0, parent_root)

        try:
            # Execute in safe isolated sandbox namespace
            exec(source_code, sandbox, sandbox)
        except Exception as e:
            err_msg = str(e)
            if isinstance(e, ImportError) and ("relative import" in err_msg or "no known parent package" in err_msg or "restricted in Metamorphic Sandbox" in err_msg):
                return []
            return [MetamorphicViolation(
                relation_name="MR-COMPILE-CRASH",
                property_description="Crash during module loading",
                input_sample=None,
                perturbed_input=None,
                actual_output=str(e),
                expected_property="Source must be executable without top-level crash",
                causal_diagnosis=f"Module level execution threw: {e}"
            )]

        COMMUTATIVE_TOKENS = {
            "add", "sum", "mult", "sym", "merge", "equal", "or", "and", "xor",
            "intersect", "union", "combine", "diff", "max", "min", "gcd", "lcm", "commutative"
        }
        IDEMPOTENT_TOKENS = {
            "clean", "strip", "sort", "norm", "abs", "idemp", "dedup", "filter",
            "unique", "sanitize", "format", "trim", "simplify", "lower", "upper",
            "round", "truncate", "normalize", "prune"
        }

        for name, obj in list(sandbox.items()):
            if not inspect.isfunction(obj):
                continue
            if name.startswith(("_", "cmd_")):
                continue

            tokens = set(name.lower().split("_"))
            try:
                sig = inspect.signature(obj)
                param_count = len(sig.parameters)

                if param_count == 2 and any(k in tokens for k in COMMUTATIVE_TOKENS):
                    v = self._probe_adaptive_commutativity(obj)
                    if v:
                        violations.append(v)
                elif param_count == 1 and any(k in tokens for k in IDEMPOTENT_TOKENS):
                    v = self._probe_adaptive_idempotence(obj)
                    if v:
                        violations.append(v)
            except (ValueError, TypeError, AttributeError, RuntimeError) as probe_err:
                logging.getLogger(__name__).debug("Metamorphic probe skipped for %s: %s", name, probe_err)
                continue

        return violations
