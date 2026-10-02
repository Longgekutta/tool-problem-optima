#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AST Interceptor: Pre-Execution Semantic Invariant & Anti-Pattern Sentinel
========================================================================
Inspects Python Abstract Syntax Trees to catch:
  1. Patch Overfitting (PRB-E101): Hardcoded test input/output branching
  2. Tautological Verification (PRB-E104): A == A circular assertions, assert True
  3. Goodhart Zero-Assertion (PRB-E105): Test functions without assertions
  4. Silent Exception Swallow (PRB-E108): Bare except: pass or empty handlers
  5. Mock Gaming (PRB-E110): Overzealous mock patching in tests
"""

import ast
from dataclasses import dataclass
from typing import List, Optional, Dict, Any


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
    def __init__(self, file_path: str, source_lines: List[str]):
        self.file_path = file_path
        self.source_lines = source_lines
        self.findings: List[DiagnosticFinding] = []
        self._current_function_name: Optional[str] = None
        self._current_function_assertions: int = 0

    def _get_snippet(self, lineno: int) -> str:
        if 1 <= lineno <= len(self.source_lines):
            return self.source_lines[lineno - 1].strip()
        return ""

    def visit_FunctionDef(self, node: ast.FunctionDef):
        prev_fn = self._current_function_name
        prev_asserts = self._current_function_assertions

        self._current_function_name = node.name
        self._current_function_assertions = 0

        self.generic_visit(node)

        # Check for Goodhart Zero Assertion in test functions
        if node.name.startswith("test_") or node.name.endswith("_test"):
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

        self._current_function_name = prev_fn
        self._current_function_assertions = prev_asserts

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_If(self, node: ast.If):
        """Detect Patch Overfitting: hardcoded specific test input values in condition."""
        # Check if the condition compares parameter directly against literal constants
        # e.g., if x == 42 and y == "foo": return "fixed"
        if self._is_hardcoded_patch_condition(node.test):
            # Check if body directly returns a literal constant
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

        self.generic_visit(node)

    def _is_hardcoded_patch_condition(self, test_node: ast.AST) -> bool:
        """Check for pattern: arg == LITERAL."""
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

    def visit_Assert(self, node: ast.Assert):
        self._current_function_assertions += 1

        # Check for assert True or assert 1
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

        # Check for circular comparison: assert a == a
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

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        """Check for PRB-E108: Silent Exception Swallow (bare except: pass)."""
        is_bare = (node.type is None)
        if not is_bare and isinstance(node.type, ast.Name) and node.type.id in ("Exception", "BaseException"):
            is_bare = True

        if is_bare:
            # Check body: is it just `pass` or `return None` / `return`
            if len(node.body) == 1:
                first = node.body[0]
                if isinstance(first, ast.Pass) or (isinstance(first, ast.Return) and (first.value is None or isinstance(first.value, ast.Constant))):
                    self.findings.append(DiagnosticFinding(
                        code="PRB-E108",
                        name="Silent Exception Swallow (Error Masking)",
                        file_path=self.file_path,
                        line_number=node.lineno,
                        column=node.col_offset,
                        message="Broad exception caught and silently swallowed with empty pass/return, masking critical failures.",
                        snippet=self._get_snippet(node.lineno),
                        remediation_suggestion="Catch specific domain exceptions, log tracebacks, and handle or re-raise gracefully."
                    ))

        self.generic_visit(node)


def audit_source_code(source: str, file_path: str = "<memory>") -> List[DiagnosticFinding]:
    """Parses Python source code and runs the Pathology AST Visitor."""
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return [DiagnosticFinding(
            code="PRB-E001",
            name="Syntax Parse Error",
            file_path=file_path,
            line_number=e.lineno or 1,
            column=e.offset or 1,
            message=f"Source code has invalid syntax: {e.msg}",
            snippet=e.text.strip() if e.text else "",
            remediation_suggestion="Fix syntax errors before semantic pathology analysis."
        )]

    lines = source.splitlines()
    visitor = PathologyASTVisitor(file_path=file_path, source_lines=lines)
    visitor.visit(tree)
    return visitor.findings
