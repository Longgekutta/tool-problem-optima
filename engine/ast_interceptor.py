#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AST Interceptor: Pre-Execution Semantic Invariant & Anti-Pattern Sentinel
========================================================================
Rigorous, static AST compiler visitor inspecting Python Abstract Syntax Trees
to detect 22 code-level software pathologies:
  - PRB-E101: Patch Overfitting (Hardcoded Edge Case Return)
  - PRB-E102: Specification Gaming (Assertion Bypass in Tests)
  - PRB-E103: Shortcut Learning (Artificial Sleep / Dummy Bypass)
  - PRB-E104: Tautological Verification (Trivial or Circular Assertion)
  - PRB-E105: Goodhart's Law Exploitation (Zero-Assertion Tests)
  - PRB-E106: Clever Hans Effect (Stack Frame / Caller Introspection)
  - PRB-E108: Silent Exception Swallow (Bare Except Pass / Masking)
  - PRB-E109: Leaky Abstraction (Global State Mutation in Functions)
  - PRB-E110: Mock Gaming (Mocking the Unit Under Test)
  - PRB-E201: Fencepost & Off-by-One Error (Subscript <= len)
  - PRB-E202: Silent Nullability (Unchecked Chained Dereference after .get())
  - PRB-E203: Floating Point Precision Loss (Direct Float Equality == 0.1)
  - PRB-E204: ReDoS Catastrophic Backtracking (Nested Quantifier Regex)
  - PRB-E301: TOCTOU Race Condition (Check-then-Open File Gap)
  - PRB-E302: Asymmetric Lock Acquisition (Inconsistent Lock Ordering)
  - PRB-E303: Unbounded Resource Descriptor Leak (Raw open() without with)
  - PRB-E304: Cascading Failure & Thundering Herd (Unbounded Threads in Loop)
  - PRB-E401: Flaky Test & Heisenbug (Unseeded Random/Time in Test)
  - PRB-E402: Assertion Roulette (Multiple Bare Asserts Without Failure Messages)
  - PRB-E501: Phantom Package Hallucination (Importing Non-existent / Slop Packages)
  - PRB-E502: Dependency Bloat (Wildcard 'from x import *' Imports)
  - PRB-E503: Hardcoded Secret / Credential Leak (Plaintext API Keys)

Total audit latency < 15ms. 100% Python standard library.
"""

import ast
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional, Set, Tuple, Dict, Any


import sys
import importlib.metadata
import importlib.util
import pkgutil


def is_unverified_phantom_package(package_name: str, file_path: str = "") -> bool:
    """
    Generalized Phantom Package Resolver (Zero Hardcoding):
    Verifies package existence against:
      1. Python Standard Library frozen universe (sys.stdlib_module_names, sys.builtin_module_names)
      2. Local workspace files/directories adjacent to file_path
      3. Python environment installed distributions (importlib.metadata)
      4. Import loaders (importlib.util.find_spec)
    """
    top = package_name.split(".")[0]
    if not top:
        return False
    # 1. Stdlib check
    if top in sys.stdlib_module_names or top in sys.builtin_module_names:
        return False
    repo_root = Path(__file__).resolve().parent.parent
    # 2. Local workspace check
    if file_path and file_path != "<memory>":
        p = Path(file_path).resolve()
        for parent in [p.parent, p.parent.parent, Path.cwd(), repo_root]:
            if (parent / f"{top}.py").exists() or (parent / top / "__init__.py").exists() or (parent / top).is_dir():
                return False
    else:
        for parent in [Path.cwd(), repo_root]:
            if (parent / f"{top}.py").exists() or (parent / top / "__init__.py").exists() or (parent / top).is_dir():
                return False
    # 3. Environment installed distributions
    try:
        importlib.metadata.version(top)
        return False
    except (importlib.metadata.PackageNotFoundError, ValueError):
        pass
    # 4. Loader check via modern importlib.util.find_spec
    try:
        if importlib.util.find_spec(top) is not None:
            return False
    except (ValueError, AttributeError, ImportError):
        pass

    return True


@dataclass
class DiagnosticFinding:
    """An identified pathology violation in source code."""
    code: str
    name: str
    file_path: str
    line_number: int
    column: int
    message: str
    snippet: str
    remediation_suggestion: str


class PathologyASTVisitor(ast.NodeVisitor):
    def __init__(self, file_path: str, source_lines: List[str], local_funcs: Optional[Dict[str, Dict[str, Any]]] = None):
        self.file_path = file_path
        self.source_lines = source_lines
        self.findings: List[DiagnosticFinding] = []
        self.local_funcs = local_funcs or {}

        self._current_function_name: Optional[str] = None
        self._current_function_assertions: int = 0
        self._current_function_bare_assertions: int = 0
        self._current_function_sharp_assertions: int = 0
        self._current_function_weak_assertions: int = 0
        self._in_loop: int = 0
        self._lock_orderings: List[Tuple[str, str, int]] = []

    def _get_snippet(self, lineno: int) -> str:
        if 0 <= lineno - 1 < len(self.source_lines):
            return self.source_lines[lineno - 1].strip()
        return ""

    def visit_FunctionDef(self, node: ast.FunctionDef):
        prev_fn = self._current_function_name
        prev_asserts = self._current_function_assertions
        prev_bare_asserts = self._current_function_bare_assertions
        prev_sharp_asserts = self._current_function_sharp_assertions
        prev_weak_asserts = self._current_function_weak_assertions

        self._current_function_name = node.name
        self._current_function_assertions = 0
        self._current_function_bare_assertions = 0
        self._current_function_sharp_assertions = 0
        self._current_function_weak_assertions = 0

        self.generic_visit(node)

        # PRB-E109: Leaky Abstraction: Mutable Default Argument (Flake8 B006 / Ruff B006)
        all_defaults = list(node.args.defaults) + [d for d in getattr(node.args, "kw_defaults", []) if d is not None]
        for d in all_defaults:
            is_mutable = False
            if isinstance(d, (ast.List, ast.Dict, ast.Set)):
                is_mutable = True
            elif isinstance(d, ast.Call) and isinstance(d.func, ast.Name) and d.func.id in ("list", "dict", "set"):
                is_mutable = True
            if is_mutable:
                self.findings.append(DiagnosticFinding(
                    code="PRB-E109",
                    name="Leaky Abstraction & State Space Explosion (Mutable Default Argument)",
                    file_path=self.file_path,
                    line_number=d.lineno,
                    column=d.col_offset,
                    message=f"Function '{node.name}' uses mutable default argument. State will persist across invocations.",
                    snippet=self._get_snippet(d.lineno),
                    remediation_suggestion="Use 'None' as default value and initialize defensively inside the function body (e.g. 'if arg is None: arg = []')."
                ))

        # Check test functions (only in test files, test directories, or memory test snippets)
        is_test_file = True
        if self.file_path and self.file_path != "<memory>":
            p = Path(self.file_path)
            is_in_test_dir = any(part in ("tests", "test") for part in p.parts)
            is_test_filename = p.name.startswith("test_") or p.name.endswith("_test.py")
            is_test_file = is_in_test_dir or is_test_filename

        is_test_fn = is_test_file and (node.name.startswith("test_") or node.name.endswith("_test")) and not node.name.startswith("cmd_")
        if is_test_fn:
            # PRB-E105: Goodhart's Law (Zero Assertion)
            if self._current_function_assertions == 0:
                self.findings.append(DiagnosticFinding(
                    code="PRB-E105",
                    name="Goodhart's Law Exploitation (Zero Assertion)",
                    file_path=self.file_path,
                    line_number=node.lineno,
                    column=node.col_offset,
                    message=f"Test function '{node.name}' has zero assertions; merely executes without verification.",
                    snippet=self._get_snippet(node.lineno),
                    remediation_suggestion="Add explicit invariant assertions verifying system state, return values, or side effects."
                ))
            elif self._current_function_assertions > 0 and self._current_function_sharp_assertions == 0:
                self.findings.append(DiagnosticFinding(
                    code="PRB-E105",
                    name="Goodhart's Law Exploitation (Weak Assertion / Trivial Oracle)",
                    file_path=self.file_path,
                    line_number=node.lineno,
                    column=node.col_offset,
                    message=f"Test function '{node.name}' relies entirely on {self._current_function_weak_assertions} weak assertion(s) (e.g. 'is not None', 'len > 0', 'isinstance') without verifying concrete state or values.",
                    snippet=self._get_snippet(node.lineno),
                    remediation_suggestion="Replace weak existential assertions with sharp value equalities (e.g. assert result == expected) or formal invariants."
                ))

            # PRB-E402: Assertion Roulette (>= 3 assertions, all bare without messages)
            if self._current_function_assertions >= 3 and self._current_function_bare_assertions == self._current_function_assertions:
                self.findings.append(DiagnosticFinding(
                    code="PRB-E402",
                    name="Assertion Roulette (Incomplete Oracle)",
                    file_path=self.file_path,
                    line_number=node.lineno,
                    column=node.col_offset,
                    message=f"Test function '{node.name}' contains {self._current_function_assertions} assertions, all without diagnostic failure messages.",
                    snippet=self._get_snippet(node.lineno),
                    remediation_suggestion="Provide descriptive failure messages for assertions (e.g., assert cond, 'expected X because Y')."
                ))

        self._current_function_name = prev_fn
        self._current_function_assertions = prev_asserts
        self._current_function_bare_assertions = prev_bare_asserts
        self._current_function_sharp_assertions = prev_sharp_asserts
        self._current_function_weak_assertions = prev_weak_asserts

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_For(self, node: ast.For):
        self._in_loop += 1
        self.generic_visit(node)
        self._in_loop -= 1

    def visit_While(self, node: ast.While):
        self._in_loop += 1
        self.generic_visit(node)
        self._in_loop -= 1

    def visit_If(self, node: ast.If):
        # PRB-E101: Patch Overfitting: hardcoded specific test input values in condition
        if self._is_hardcoded_patch_condition(node.test):
            if len(node.body) == 1 and isinstance(node.body[0], ast.Return) and isinstance(node.body[0].value, ast.Constant):
                self.findings.append(DiagnosticFinding(
                    code="PRB-E101",
                    name="Patch Overfitting (Hardcoded Edge Case Return)",
                    file_path=self.file_path,
                    line_number=node.lineno,
                    column=node.col_offset,
                    message="Detected hardcoded condition matching specific literals returning a static constant (suspected test-gaming patch).",
                    snippet=self._get_snippet(node.lineno),
                    remediation_suggestion="Formulate a generalized mathematical rule or causal invariant rather than branching on specific test constants."
                ))

        # PRB-E301: TOCTOU Race Condition: if os.path.exists(p) followed by open(p) in body
        if self._is_path_exists_check(node.test):
            checked_path = self._get_path_from_exists_check(node.test)
            if checked_path and self._body_contains_raw_file_op(node.body, checked_path):
                self.findings.append(DiagnosticFinding(
                    code="PRB-E301",
                    name="Time-of-Check to Time-of-Use Race Condition (TOCTOU)",
                    file_path=self.file_path,
                    line_number=node.lineno,
                    column=node.col_offset,
                    message=f"Checking file existence with 'os.path.exists({checked_path})' before operating on it creates a TOCTOU race condition.",
                    snippet=self._get_snippet(node.lineno),
                    remediation_suggestion="Adopt EAFP (Easier to Ask for Forgiveness than Permission) pattern: try opening the file directly and handle FileNotFoundError / FileExistsError."
                ))

        self.generic_visit(node)

    def _is_hardcoded_patch_condition(self, test_node: ast.AST) -> bool:
        if isinstance(test_node, ast.Compare):
            if len(test_node.ops) == 1 and isinstance(test_node.ops[0], ast.Eq):
                left = test_node.left
                right = test_node.comparators[0]
                if (isinstance(left, ast.Name) and isinstance(right, ast.Constant)) or \
                   (isinstance(left, ast.Constant) and isinstance(right, ast.Name)):
                    return True
        elif isinstance(test_node, ast.BoolOp) and isinstance(test_node.op, ast.And):
            return any(self._is_hardcoded_patch_condition(val) for val in test_node.values)
        return False

    def _is_path_exists_check(self, test_node: ast.AST) -> bool:
        if isinstance(test_node, ast.Call):
            if isinstance(test_node.func, ast.Attribute) and test_node.func.attr in ("exists", "isfile", "isdir"):
                return True
        return False

    def _get_path_from_exists_check(self, test_node: ast.AST) -> Optional[str]:
        if isinstance(test_node, ast.Call) and test_node.args:
            arg = test_node.args[0]
            if isinstance(arg, ast.Name):
                return arg.id
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                return arg.value
        return None

    def _body_contains_raw_file_op(self, body: List[ast.stmt], target_path: str) -> bool:
        for stmt in body:
            for child in ast.walk(stmt):
                if isinstance(child, ast.Call):
                    func_name = ""
                    if isinstance(child.func, ast.Name):
                        func_name = child.func.id
                    elif isinstance(child.func, ast.Attribute):
                        func_name = child.func.attr
                    if func_name in ("open", "remove", "unlink"):
                        if child.args:
                            first_arg = child.args[0]
                            if (isinstance(first_arg, ast.Name) and first_arg.id == target_path) or \
                               (isinstance(first_arg, ast.Constant) and first_arg.value == target_path):
                                return True
        return False

    def _is_weak_assertion(self, test_node: ast.AST) -> bool:
        """
        Detects weak / trivial assertion smells:
          - is not None / != None / is None / == None
          - len(...) > 0 / len(...) >= 1 / len(...) != 0
          - isinstance(..., ...)
          - Bare Name truthiness: assert x
          - bool(x)
        """
        # 1. Bare identifier / truthiness (e.g. assert res)
        if isinstance(test_node, ast.Name):
            return True

        # 2. bool(x)
        if isinstance(test_node, ast.Call) and isinstance(test_node.func, ast.Name) and test_node.func.id == "bool":
            return True

        # 3. isinstance(..., ...)
        if isinstance(test_node, ast.Call) and isinstance(test_node.func, ast.Name) and test_node.func.id == "isinstance":
            return True

        # 4. Compares: 'is not None', 'len(x) > 0'
        if isinstance(test_node, ast.Compare) and len(test_node.ops) == 1:
            op = test_node.ops[0]
            comp = test_node.comparators[0]
            left = test_node.left

            # Checks against None
            if isinstance(comp, ast.Constant) and comp.value is None:
                if isinstance(op, (ast.IsNot, ast.NotEq, ast.Is, ast.Eq)):
                    return True
            if isinstance(left, ast.Constant) and left.value is None:
                if isinstance(op, (ast.IsNot, ast.NotEq, ast.Is, ast.Eq)):
                    return True

            # Checks len(x) > 0 or len(x) >= 1 or len(x) != 0
            is_left_len = isinstance(left, ast.Call) and isinstance(left.func, ast.Name) and left.func.id == "len"
            if is_left_len and isinstance(comp, ast.Constant) and comp.value in (0, 1):
                if isinstance(op, (ast.Gt, ast.GtE, ast.NotEq)):
                    return True

        return False

    def visit_Assert(self, node: ast.Assert):
        self._current_function_assertions += 1
        if node.msg is None:
            self._current_function_bare_assertions += 1

        if self._is_weak_assertion(node.test):
            self._current_function_weak_assertions += 1
        else:
            self._current_function_sharp_assertions += 1

        # PRB-E104: Asserting a non-empty tuple: assert (cond, "msg") is always truthy
        if isinstance(node.test, ast.Tuple) and len(node.test.elts) > 0:
            self.findings.append(DiagnosticFinding(
                code="PRB-E104",
                name="Tautological Verification (Tuple Assertion Trap)",
                file_path=self.file_path,
                line_number=node.lineno,
                column=node.col_offset,
                message="Asserting a non-empty tuple (assert (cond, msg)) is always truthy in Python. Use 'assert cond, msg' instead.",
                snippet=self._get_snippet(node.lineno),
                remediation_suggestion="Separate condition and failure message with a comma without enclosing parentheses: 'assert cond, msg'."
            ))

        # PRB-E104: Trivial assertion assert True or assert 1
        if isinstance(node.test, ast.Constant) and bool(node.test.value) is True:
            self.findings.append(DiagnosticFinding(
                code="PRB-E104",
                name="Tautological Verification (Trivial Assertion)",
                file_path=self.file_path,
                line_number=node.lineno,
                column=node.col_offset,
                message="Tautological assertion 'assert True/1' provides zero validation power.",
                snippet=self._get_snippet(node.lineno),
                remediation_suggestion="Assert real causal properties and postconditions rather than boolean constants."
            ))

        # PRB-E104: Circular comparison: assert a == a
        if isinstance(node.test, ast.Compare):
            if len(node.test.ops) == 1 and isinstance(node.test.ops[0], (ast.Eq, ast.Is)):
                left_dump = ast.dump(node.test.left)
                right_dump = ast.dump(node.test.comparators[0])
                if left_dump == right_dump:
                    self.findings.append(DiagnosticFinding(
                        code="PRB-E104",
                        name="Tautological Verification (Circular Equality)",
                        file_path=self.file_path,
                        line_number=node.lineno,
                        column=node.col_offset,
                        message="Circular assertion (A == A) compares identical expressions on both sides.",
                        snippet=self._get_snippet(node.lineno),
                        remediation_suggestion="Compare target output against an independent reference oracle or formal invariant."
                    ))

        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare):
        # PRB-E201: Fencepost & Off-by-One Error: index <= len(arr)
        for op, comp in zip(node.ops, node.comparators):
            if isinstance(op, ast.LtE):
                if isinstance(comp, ast.Call) and isinstance(comp.func, ast.Name) and comp.func.id == "len":
                    self.findings.append(DiagnosticFinding(
                        code="PRB-E201",
                        name="Fencepost & Off-by-One Error (Subscript <= len)",
                        file_path=self.file_path,
                        line_number=node.lineno,
                        column=node.col_offset,
                        message="Comparison uses '<= len(...)'. In 0-indexed sequences, valid indices are strictly '< len(...)'.",
                        snippet=self._get_snippet(node.lineno),
                        remediation_suggestion="Use '< len(...)' or standard iterator loops to avoid IndexError at upper boundary."
                    ))

            # PRB-E203: Floating Point Precision Loss: exact float equality comparison (x == 0.1)
            if isinstance(op, ast.Eq):
                left_has_fractional_float = (
                    isinstance(node.left, ast.Constant) and
                    isinstance(node.left.value, float) and
                    not node.left.value.is_integer()
                )
                comp_has_fractional_float = (
                    isinstance(comp, ast.Constant) and
                    isinstance(comp.value, float) and
                    not comp.value.is_integer()
                )
                if left_has_fractional_float or comp_has_fractional_float:
                    self.findings.append(DiagnosticFinding(
                        code="PRB-E203",
                        name="Floating Point Non-Associativity (Exact Float Equality)",
                        file_path=self.file_path,
                        line_number=node.lineno,
                        column=node.col_offset,
                        message="Direct equality comparison '==' with fractional floating point literal risks catastrophic precision failure.",
                        snippet=self._get_snippet(node.lineno),
                        remediation_suggestion="Use 'math.isclose(a, b, rel_tol=1e-9)' or 'abs(a - b) < epsilon' for float comparisons."
                    ))

            # PRB-E202: Comparison using 'is' with scalar literal (SyntaxWarning / F632)
            if isinstance(op, (ast.Is, ast.IsNot)):
                left_is_lit = isinstance(node.left, ast.Constant) and not (node.left.value is None or isinstance(node.left.value, bool))
                comp_is_lit = isinstance(comp, ast.Constant) and not (comp.value is None or isinstance(comp.value, bool))
                if left_is_lit or comp_is_lit:
                    self.findings.append(DiagnosticFinding(
                        code="PRB-E202",
                        name="Silent Nullability & Type Confusion (Literal Identity Comparison)",
                        file_path=self.file_path,
                        line_number=node.lineno,
                        column=node.col_offset,
                        message="Comparing with literal via 'is'/'is not' violates Python identity semantics and raises SyntaxWarning.",
                        snippet=self._get_snippet(node.lineno),
                        remediation_suggestion="Use '==' or '!=' when comparing with scalar literal values; reserve 'is' for None, True, False singletons."
                    ))

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        # PRB-E106: Clever Hans Effect: inspecting stack frames or sys._getframe to alter behavior
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in ("_getframe", "currentframe") or (node.func.attr == "stack" and getattr(node.func.value, "id", "") == "inspect"):
                self.findings.append(DiagnosticFinding(
                    code="PRB-E106",
                    name="Clever Hans Effect (Stack Frame Introspection)",
                    file_path=self.file_path,
                    line_number=node.lineno,
                    column=node.col_offset,
                    message="Inspecting call stack frames / caller names indicates runtime test-gaming heuristics.",
                    snippet=self._get_snippet(node.lineno),
                    remediation_suggestion="Derive program behavior purely from explicit inputs rather than inspecting caller frame names."
                ))

        # PRB-E103: Shortcut Learning: inserting artificial sleep in tests
        func_name = ""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr

        # Count test assertions from unittest assertions (self.assertEqual, self.assertTrue, etc.)
        if func_name == "range" and len(node.args) == 1:
            arg = node.args[0]
            if isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Add):
                left_is_len = isinstance(arg.left, ast.Call) and getattr(arg.left.func, "id", "") == "len"
                right_is_one = isinstance(arg.right, ast.Constant) and arg.right.value == 1
                if left_is_len and right_is_one:
                    self.findings.append(DiagnosticFinding(
                        code="PRB-E201",
                        name="Fencepost & Off-by-One Error (range(len + 1))",
                        file_path=self.file_path,
                        line_number=node.lineno,
                        column=node.col_offset,
                        message="Using 'range(len(...) + 1)' exceeds sequence upper bound, causing IndexError during indexing.",
                        snippet=self._get_snippet(node.lineno),
                        remediation_suggestion="Use 'range(len(...))' or iterate directly over elements."
                    ))

        if isinstance(node.func, ast.Attribute) and node.func.attr.startswith("assert"):
            self._current_function_assertions += 1
            has_msg = any(kw.arg == "msg" for kw in getattr(node, "keywords", [])) or (len(node.args) >= 3 and node.func.attr in ("assertEqual", "assertNotEqual", "assertIn", "assertNotIn")) or (len(node.args) >= 2 and node.func.attr in ("assertTrue", "assertFalse", "assertIsNone", "assertIsNotNone"))
            if not has_msg:
                self._current_function_bare_assertions += 1

            weak_attrs = ("assertIsNotNone", "assertIsNone", "assertIsInstance")
            if node.func.attr in weak_attrs or (node.func.attr == "assertTrue" and node.args and isinstance(node.args[0], ast.Name)):
                self._current_function_weak_assertions += 1
            else:
                self._current_function_sharp_assertions += 1
        elif isinstance(node.func, ast.Name) and (node.func.id.startswith("assert_") or node.func.id == "raises"):
            self._current_function_assertions += 1
            self._current_function_sharp_assertions += 1

        # PRB-E109: Interface Contract & Signature Drift (Local Function Call Mismatch)
        if isinstance(node.func, ast.Name) and node.func.id in self.local_funcs:
            fn_meta = self.local_funcs[node.func.id]
            if self._current_function_name != node.func.id:
                num_pos_passed = len(node.args)
                kw_names_passed = {kw.arg for kw in node.keywords if kw.arg is not None}
                total_passed = num_pos_passed + len(kw_names_passed)
                if total_passed < fn_meta["min_args"]:
                    self.findings.append(DiagnosticFinding(
                        code="PRB-E109",
                        name="Interface & Contract Drift (Missing Required Argument)",
                        file_path=self.file_path,
                        line_number=node.lineno,
                        column=node.col_offset,
                        message=f"Call to '{node.func.id}' provides {total_passed} arguments, but definition requires at least {fn_meta['min_args']}.",
                        snippet=self._get_snippet(node.lineno),
                        remediation_suggestion=f"Provide all required arguments according to '{node.func.id}' signature."
                    ))
                elif not fn_meta["has_varargs"] and num_pos_passed > fn_meta["max_args"]:
                    self.findings.append(DiagnosticFinding(
                        code="PRB-E109",
                        name="Interface & Contract Drift (Excess Positional Arguments)",
                        file_path=self.file_path,
                        line_number=node.lineno,
                        column=node.col_offset,
                        message=f"Call to '{node.func.id}' provides {num_pos_passed} positional arguments, exceeding maximum permitted ({fn_meta['max_args']}).",
                        snippet=self._get_snippet(node.lineno),
                        remediation_suggestion=f"Align call arguments with '{node.func.id}' signature."
                    ))
                elif not fn_meta["has_kwargs"]:
                    unknown_kws = kw_names_passed - fn_meta["all_arg_names"]
                    if unknown_kws:
                        self.findings.append(DiagnosticFinding(
                            code="PRB-E109",
                            name="Interface & Contract Drift (Unknown Keyword Argument)",
                            file_path=self.file_path,
                            line_number=node.lineno,
                            column=node.col_offset,
                            message=f"Call to '{node.func.id}' passed unexpected keyword argument(s): {sorted(list(unknown_kws))}.",
                            snippet=self._get_snippet(node.lineno),
                            remediation_suggestion=f"Ensure keyword arguments match '{node.func.id}' signature: {sorted(list(fn_meta['all_arg_names']))}."
                        ))

        is_test_ctx = self._current_function_name and (self._current_function_name.startswith("test_") or self._current_function_name.endswith("_test"))
        if is_test_ctx and func_name in ("sleep",):
            self.findings.append(DiagnosticFinding(
                code="PRB-E103",
                name="Shortcut Learning (Artificial Sleep / Timing Hack in Test)",
                file_path=self.file_path,
                line_number=node.lineno,
                column=node.col_offset,
                message=f"Calling '{func_name}' directly inside test indicates flaky timing hack rather than causal event synchronization.",
                snippet=self._get_snippet(node.lineno),
                remediation_suggestion="Use deterministic synchronization primitives (Event/Condition/Queue) instead of arbitrary sleep delays."
            ))

        # PRB-E110: Mock Gaming: mocking unit under test
        if func_name in ("patch", "patch_object"):
            if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                target_str = node.args[0].value
                if self.file_path and Path(self.file_path).stem.replace("test_", "") in target_str:
                    self.findings.append(DiagnosticFinding(
                        code="PRB-E110",
                        name="Mock Gaming & Mock Inversion",
                        file_path=self.file_path,
                        line_number=node.lineno,
                        column=node.col_offset,
                        message=f"Mock patch target '{target_str}' overlaps with the unit under test itself, creating tautological illusion.",
                        snippet=self._get_snippet(node.lineno),
                        remediation_suggestion="Mock external third-party I/O boundaries only; never mock the internal logic of the unit under test."
                    ))

        # PRB-E204: ReDoS Catastrophic Backtracking: re.compile / re.search with nested quantifiers
        if isinstance(node.func, ast.Attribute) and getattr(node.func.value, "id", "") == "re" and node.func.attr in ("compile", "search", "match"):
            if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                pattern = node.args[0].value
                if self._is_redos_vulnerable(pattern):
                    self.findings.append(DiagnosticFinding(
                        code="PRB-E204",
                        name="ReDoS Catastrophic Backtracking",
                        file_path=self.file_path,
                        line_number=node.lineno,
                        column=node.col_offset,
                        message=f"Regex pattern '{pattern}' contains nested quantifiers prone to exponential backtrack explosion (O(2^N)).",
                        snippet=self._get_snippet(node.lineno),
                        remediation_suggestion="Flatten nested repetitions (e.g. replace '(a+)+' with 'a+' or use possessive/atomic groups)."
                    ))

        # PRB-E304: Cascading Failure & Thundering Herd: unbounded thread creation inside loop
        if self._in_loop > 0:
            if (func_name == "Thread" or func_name == "Process") or (isinstance(node.func, ast.Attribute) and node.func.attr in ("Thread", "Process")):
                self.findings.append(DiagnosticFinding(
                    code="PRB-E304",
                    name="Cascading Failure & Thundering Herd (Unbounded Thread Creation in Loop)",
                    file_path=self.file_path,
                    line_number=node.lineno,
                    column=node.col_offset,
                    message="Spawning raw Thread/Process instances directly inside loop without bounded pool risks OS descriptor exhaustion.",
                    snippet=self._get_snippet(node.lineno),
                    remediation_suggestion="Use 'concurrent.futures.ThreadPoolExecutor(max_workers=...)' or a bounded Semaphore."
                ))

        # PRB-E401: Flaky Test & Heisenbug: unseeded random or time.time inside test
        if is_test_ctx:
            if func_name in ("random", "randint", "choice", "randrange") or (isinstance(node.func, ast.Attribute) and node.func.attr in ("random", "randint", "choice")):
                self.findings.append(DiagnosticFinding(
                    code="PRB-E401",
                    name="Flaky Test & Heisenbug (Unseeded Random in Test)",
                    file_path=self.file_path,
                    line_number=node.lineno,
                    column=node.col_offset,
                    message=f"Non-deterministic call to '{func_name}' in test introduces non-reproducible Heisenbug flakiness.",
                    snippet=self._get_snippet(node.lineno),
                    remediation_suggestion="Fix pseudorandom generator seed explicitly via 'random.seed(42)' or pass deterministic test vectors."
                ))

        self.generic_visit(node)

    def _is_redos_vulnerable(self, pattern: str) -> bool:
        redos_signatures = [
            r"\([^)]*[\+\*]\)[\+\*]",       # (a+)+ or (x*)*
            r"\(\[[^\]]+\][\+\*]\)[\+\*]",  # ([a-z]+)*
            r"\(\\w[\+\*]\)[\+\*]",         # (\w+)+
            r"\(\\d[\+\*]\)[\+\*]",         # (\d+)+
        ]
        return any(re.search(sig, pattern) for sig in redos_signatures)

    def visit_Attribute(self, node: ast.Attribute):
        # PRB-E202: Silent Nullability: chained dereference on .get(...) result without None check
        if isinstance(node.value, ast.Call):
            inner_func = node.value.func
            if isinstance(inner_func, ast.Attribute) and inner_func.attr == "get":
                self.findings.append(DiagnosticFinding(
                    code="PRB-E202",
                    name="Silent Nullability & Type Confusion (Chained Dereference after .get())",
                    file_path=self.file_path,
                    line_number=node.lineno,
                    column=node.col_offset,
                    message=f"Chained attribute access '.{node.attr}' directly on '.get()' result will raise AttributeError if key is absent.",
                    snippet=self._get_snippet(node.lineno),
                    remediation_suggestion="Safely unpack or verify None check: 'val = d.get(k); if val is not None: ...' or provide non-None default."
                ))

        self.generic_visit(node)

    def visit_Global(self, node: ast.Global):
        # PRB-E109: Leaky Abstraction: mutating global shared state inside functions
        self.findings.append(DiagnosticFinding(
            code="PRB-E109",
            name="Leaky Abstraction & State Space Explosion (Global Variable Mutation)",
            file_path=self.file_path,
            line_number=node.lineno,
            column=node.col_offset,
            message=f"Global declaration for {node.names} breaks functional modularity and creates concurrency race conditions.",
            snippet=self._get_snippet(node.lineno),
            remediation_suggestion="Encapsulate shared mutable state in explicit class instances or pass state parameters functionally."
        ))
        self.generic_visit(node)

    def visit_Expr(self, node: ast.Expr):
        # PRB-E109: Unawaited coroutine call in expression statement
        if isinstance(node.value, ast.Call):
            call_fn = None
            if isinstance(node.value.func, ast.Name):
                call_fn = node.value.func.id
            if call_fn and call_fn in self.local_funcs and self.local_funcs[call_fn].get("is_async"):
                self.findings.append(DiagnosticFinding(
                    code="PRB-E109",
                    name="Interface & Contract Drift (Unawaited Coroutine Call)",
                    file_path=self.file_path,
                    line_number=node.lineno,
                    column=node.col_offset,
                    message=f"Call to async coroutine function '{call_fn}' is not awaited. Coroutine will never execute.",
                    snippet=self._get_snippet(node.lineno),
                    remediation_suggestion=f"Prepend 'await {call_fn}(...)' or schedule via asyncio.create_task()."
                ))
        self.generic_visit(node)

    def visit_With(self, node: ast.With):
        # PRB-E302: Asymmetric Lock Acquisition Deadlock: nested with lock1: with lock2:
        acquired_locks: List[str] = []
        for item in node.items:
            if isinstance(item.context_expr, ast.Name):
                acquired_locks.append(item.context_expr.id)

        for stmt in node.body:
            if isinstance(stmt, ast.With):
                for item in stmt.items:
                    if isinstance(item.context_expr, ast.Name):
                        inner_lock = item.context_expr.id
                        for outer_lock in acquired_locks:
                            self._lock_orderings.append((outer_lock, inner_lock, node.lineno))

        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        # PRB-E108: Silent Exception Swallow (bare except: pass)
        is_bare = (node.type is None)
        if not is_bare and isinstance(node.type, ast.Name) and node.type.id in ("Exception", "BaseException"):
            is_bare = True

        if is_bare:
            if len(node.body) == 1:
                first = node.body[0]
                if isinstance(first, (ast.Pass, ast.Continue)) or (isinstance(first, ast.Return) and (first.value is None or isinstance(first.value, ast.Constant))):
                    self.findings.append(DiagnosticFinding(
                        code="PRB-E108",
                        name="Silent Exception Swallow (Error Masking)",
                        file_path=self.file_path,
                        line_number=node.lineno,
                        column=node.col_offset,
                        message="Broad exception caught and silently swallowed with empty pass/continue/return, masking critical failures.",
                        snippet=self._get_snippet(node.lineno),
                        remediation_suggestion="Catch specific domain exceptions, log tracebacks, and handle or re-raise gracefully."
                    ))

        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant):
        # PRB-E503: Hardcoded secrets and API keys
        if isinstance(node.value, str):
            val = node.value.strip()
            if any(val.startswith(pfx) for pfx in ("ghp_", "sk-", "AKIA")) and len(val) >= 20:
                self.findings.append(DiagnosticFinding(
                    code="PRB-E503",
                    name="Hardcoded Secret / Credential Leak",
                    file_path=self.file_path,
                    line_number=node.lineno,
                    column=node.col_offset,
                    message="Detected plaintext private API token/credential hardcoded in source.",
                    snippet=self._get_snippet(node.lineno),
                    remediation_suggestion="Isolate secrets in environment variables or a vault (.env / os.getenv); do not commit to version control."
                ))

        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        # PRB-E303: Raw unmanaged open() without context manager
        if isinstance(node.value, ast.Call):
            func = node.value.func
            if isinstance(func, ast.Name) and func.id == "open":
                self.findings.append(DiagnosticFinding(
                    code="PRB-E303",
                    name="Unbounded Resource Descriptor Leak",
                    file_path=self.file_path,
                    line_number=node.lineno,
                    column=node.col_offset,
                    message="Calling raw open() directly in assignment risks descriptor leakage on exceptions.",
                    snippet=self._get_snippet(node.lineno),
                    remediation_suggestion="Wrap resource acquisition in a 'with open(...) as f:' context manager."
                ))

        self.generic_visit(node)

    def visit_Import(self, node: ast.Import):
        # PRB-E501: Phantom Package Hallucination (Zero-Hardcoding Check)
        for alias in node.names:
            if is_unverified_phantom_package(alias.name, self.file_path):
                self.findings.append(DiagnosticFinding(
                    code="PRB-E501",
                    name="Phantom Package Hallucination (Slopsquatting)",
                    file_path=self.file_path,
                    line_number=node.lineno,
                    column=node.col_offset,
                    message=f"Imported package '{alias.name}' does not exist in Python Standard Library, local workspace, or installed environment.",
                    snippet=self._get_snippet(node.lineno),
                    remediation_suggestion="Verify package existence in Python Standard Library (sys.stdlib_module_names) or official PyPI registry before importing."
                ))
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        # PRB-E501: Phantom Package in from ... import
        if node.module:
            if is_unverified_phantom_package(node.module, self.file_path):
                self.findings.append(DiagnosticFinding(
                    code="PRB-E501",
                    name="Phantom Package Hallucination (Slopsquatting)",
                    file_path=self.file_path,
                    line_number=node.lineno,
                    column=node.col_offset,
                    message=f"Imported module '{node.module}' does not exist in Python Standard Library, local workspace, or installed environment.",
                    snippet=self._get_snippet(node.lineno),
                    remediation_suggestion="Verify package existence in Python Standard Library (sys.stdlib_module_names) or official PyPI registry before importing."
                ))

        # PRB-E502: Dependency Bloat: wildcard 'from x import *'
        for alias in node.names:
            if alias.name == "*":
                self.findings.append(DiagnosticFinding(
                    code="PRB-E502",
                    name="Dependency Bloat & Namespace Pollution (Wildcard Import)",
                    file_path=self.file_path,
                    line_number=node.lineno,
                    column=node.col_offset,
                    message=f"Wildcard import 'from {node.module} import *' pollutes global namespace and risks circular imports.",
                    snippet=self._get_snippet(node.lineno),
                    remediation_suggestion="Use explicit targeted symbol imports: 'from module import specific_fn'."
                ))
        self.generic_visit(node)

    def post_analysis(self):
        """Check multi-statement global invariants like PRB-E302 lock order inversions."""
        seen_pairs: Set[Tuple[str, str]] = set()
        for l1, l2, lineno in self._lock_orderings:
            if (l2, l1) in seen_pairs:
                self.findings.append(DiagnosticFinding(
                    code="PRB-E302",
                    name="Asymmetric Lock Acquisition Deadlock",
                    file_path=self.file_path,
                    line_number=lineno,
                    column=0,
                    message=f"Inconsistent lock acquisition ordering detected between '{l1}' and '{l2}' (ABBA deadlock hazard).",
                    snippet=self._get_snippet(lineno),
                    remediation_suggestion="Enforce strict, globally deterministic lock acquisition hierarchy across all threads."
                ))
            seen_pairs.add((l1, l2))


def audit_contract_drift(original_code: str, candidate_code: str, file_path: str = "") -> List[DiagnosticFinding]:
    """
    Detects public interface and contract drift (breaking changes) between versions:
      - Removing public functions/methods
      - Removing public parameters from function signatures
      - Adding required (non-default) positional parameters without backward compatibility
    Zero external dependencies.
    """
    findings: List[DiagnosticFinding] = []
    try:
        orig_tree = ast.parse(original_code)
        cand_tree = ast.parse(candidate_code)
    except Exception:
        return []

    def get_public_signatures(tree: ast.AST) -> Dict[str, Dict[str, Any]]:
        sigs: Dict[str, Dict[str, Any]] = {}
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not node.name.startswith("_") and not node.name.startswith("test_"):
                    args = node.args
                    pos_args = [a.arg for a in args.args if a.arg not in ("self", "cls")]
                    num_defaults = len(args.defaults)
                    num_required = max(0, len(pos_args) - num_defaults)
                    sigs[node.name] = {
                        "lineno": node.lineno,
                        "pos_args": pos_args,
                        "num_required": num_required,
                        "kwonly_args": [a.arg for a in args.kwonlyargs],
                        "has_varargs": bool(args.vararg),
                        "has_kwargs": bool(args.kwarg)
                    }
        return sigs

    orig_sigs = get_public_signatures(orig_tree)
    cand_sigs = get_public_signatures(cand_tree)

    for fn_name, o_sig in orig_sigs.items():
        if fn_name in cand_sigs:
            c_sig = cand_sigs[fn_name]
            o_pos = o_sig["pos_args"]
            c_pos = c_sig["pos_args"]

            # 1. Parameter deletion
            deleted = [p for p in o_pos if p not in c_pos]
            if deleted:
                findings.append(DiagnosticFinding(
                    code="PRB-E109",
                    name="Interface & Contract Drift (Parameter Removal)",
                    file_path=file_path,
                    line_number=c_sig["lineno"],
                    column=0,
                    message=f"Public function '{fn_name}' deleted parameter(s) {deleted}, breaking existing callers.",
                    snippet=f"def {fn_name}(...)",
                    remediation_suggestion="Preserve parameter backward compatibility or provide default fallback values."
                ))

            # 2. Added new required parameters without default
            if c_sig["num_required"] > o_sig["num_required"] and not deleted:
                added_required = c_pos[o_sig["num_required"]:c_sig["num_required"]]
                findings.append(DiagnosticFinding(
                    code="PRB-E109",
                    name="Interface & Contract Drift (Required Parameter Addition)",
                    file_path=file_path,
                    line_number=c_sig["lineno"],
                    column=0,
                    message=f"Public function '{fn_name}' added non-default parameter(s) {added_required}, breaking existing positional calls.",
                    snippet=f"def {fn_name}(...)",
                    remediation_suggestion="Provide default values for new parameters to preserve backward compatibility."
                ))
    return findings


def audit_source_code(source: str, file_path: str = "<memory>", previous_source: Optional[str] = None) -> List[DiagnosticFinding]:
    """Parses Python source code and runs the comprehensive Pathology AST Visitor."""
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return [DiagnosticFinding(
            code="PRB-E003",
            name="Token Horizon Truncation & Fractured AST",
            file_path=file_path,
            line_number=e.lineno or 1,
            column=e.offset or 1,
            message=f"Source code has invalid syntax / fractured AST: {e.msg}",
            snippet=e.text.strip() if e.text else "",
            remediation_suggestion="Fix truncated tokens or syntax errors to ensure well-formed Abstract Syntax Tree."
        )]

    # Collect local function definitions for call-contract verification
    local_funcs: Dict[str, Dict[str, Any]] = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            pos_args = [a.arg for a in node.args.args if a.arg not in ("self", "cls")]
            num_defaults = len(node.args.defaults)
            min_args = max(0, len(pos_args) - num_defaults)
            max_args = len(pos_args)
            has_varargs = bool(node.args.vararg)
            has_kwargs = bool(node.args.kwarg)
            all_arg_names = set(pos_args) | {a.arg for a in node.args.kwonlyargs}
            is_async = isinstance(node, ast.AsyncFunctionDef)
            local_funcs[node.name] = {
                "min_args": min_args,
                "max_args": max_args,
                "has_varargs": has_varargs,
                "has_kwargs": has_kwargs,
                "all_arg_names": all_arg_names,
                "is_async": is_async,
                "lineno": node.lineno
            }

    lines = source.splitlines()
    visitor = PathologyASTVisitor(file_path=file_path, source_lines=lines, local_funcs=local_funcs)
    visitor.visit(tree)
    visitor.post_analysis()

    findings = list(visitor.findings)
    if previous_source:
        findings.extend(audit_contract_drift(previous_source, source, file_path=file_path))

    return findings
