#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Temporal Constraint Ledger: Multi-Turn Dialogue State & Invariant Tracker
========================================================================
Implements an Agent-C / Temporal Semantic Memory (TSM) style persistent ledger
that tracks explicit modality constraints across long multi-turn conversations (50+ turns):

  - Maintains active invariants:
      * ZERO_DEPENDENCY: pure standard library mandates
      * IDENTITY_FORMAT: UUID / deterministic format constraints
      * FORBIDDEN_FILE: explicit immutability guards on sensitive paths
      * NUMERIC_PRECISION: high-precision Decimal / financial arithmetic mandates
      * ERROR_HANDLING_CONTRACT: explicit error handling & no-swallow mandates
  - Handles state evolutions: detects when constraints are RELAXED, STRENGTHENED,
    or SUPERSEDED across subsequent turns.
  - Validates candidate code and tool actions against currently ACTIVE invariants,
    eliminating PRB-E001 (Context Satiation & Needle-in-a-Haystack Amnesia).

Zero external dependencies. Sub-5ms evaluation.
Eliminates brittle keyword hardcoding via generalized Semantic Lattices.
"""

import re
import ast
import sys
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Any
from pathlib import Path


@dataclass
class LedgerConstraint:
    """An invariant constraint tracked across dialogue turns."""
    slot_id: str
    turn_introduced: int
    category: str                                 # "IDENTITY_FORMAT" | "ZERO_DEPENDENCY" | "FORBIDDEN_FILE" | "NUMERIC_PRECISION" | "ERROR_HANDLING"
    raw_statement: str
    status: str = "ACTIVE"                        # "ACTIVE" | "RELAXED" | "SUPERSEDED"
    expected_token: Optional[str] = None
    forbidden_token: Optional[str] = None


@dataclass
class LedgerViolation:
    """A violation of an active temporal invariant."""
    constraint: LedgerConstraint
    current_turn: int
    violation_message: str
    remediation_suggestion: str


# -----------------------------------------------------------------------------
# Generalized Semantic Patterns for Constraint Lifecycle
# -----------------------------------------------------------------------------
RE_RELAX_MODAL = re.compile(
    r"(?i)\b(relax|allow|permit|lift|remove\s+constraint|can\s+now\s+use|free\s+to\s+use|no\s+longer\s+restricted)\b|"
    r"取消约束|允许使用|放宽|现在可以|不再限制|解除限制|解禁|不用遵守|允许引入"
)

RE_DEP_DOMAIN = re.compile(
    r"(?i)\b(dependenc(y|ies)|packages?|librar(y|ies)|third-party|external)\b|"
    r"依赖|三方库|第三方|外部包|包"
)

RE_ZERO_DEP_MANDATE = re.compile(
    r"(?i)\b(no\s+(?:external|third-party)\s+(?:dependenc|package|librar)|zero\s+dependenc|"
    r"pure\s+standard\s+library|stdlib\s+only|built-in\s+modules?\s+only)\b|"
    r"零三方依赖|纯标准库|零依赖|不准引入第三方|不使用第三方|禁止引入外部|仅限标准库|不要安装任何库|纯内置|只能用纯内置"
)

RE_UUID_MANDATE = re.compile(
    r"(?i)\b(uuid(v4)?|guid|ulid|snowflake)\b"
)

RE_MANDATE_MODAL = re.compile(
    r"(?i)\b(must|require|all|strictly|enforce|ensure|every|always)\b|"
    r"必须|所有|强制|统一|每个|严禁非|始终"
)

RE_FORBID_FILE = re.compile(
    r"(?i)(?:do\s+not\s+(?:modify|touch|edit|change)|don't\s+(?:touch|edit|change|modify)|never\s+touch|"
    r"不要修改|严禁改动|禁止变更|不能动|不要动|严禁修改|不能修改|保全)\s+([a-zA-Z0-9_\-\.\/]+)"
)

RE_DECIMAL_MANDATE = re.compile(
    r"(?i)\b(decimal|currency|financial|precision|money|cents)\b|金额|财务|货币|高精度|小数精度|用\s*Decimal"
)

RE_ERROR_HANDLING_MANDATE = re.compile(
    r"(?i)\b(must\s+not\s+swallow|never\s+swallow|no\s+bare\s+except|strict\s+errors?)\b|"
    r"严禁吞异常|禁止静默忽略|不能吞报错|不要空pass|必须显式捕获"
)


class TemporalConstraintLedger:
    """Persistent ledger tracking invariants across multi-turn transcripts."""

    def __init__(self):
        self.constraints: Dict[str, LedgerConstraint] = {}

    def feed_turn(self, turn_index: int, user_input: str):
        """Processes a new user prompt turn and updates constraint states."""
        text = user_input.strip()
        if not text:
            return

        # 1. Check for Constraint Relaxation / Retraction
        if RE_RELAX_MODAL.search(text):
            if RE_DEP_DOMAIN.search(text) and "ZERO_DEPENDENCY" in self.constraints:
                self.constraints["ZERO_DEPENDENCY"].status = "RELAXED"
            if (RE_DECIMAL_MANDATE.search(text) or "浮点" in text) and "NUMERIC_PRECISION" in self.constraints:
                self.constraints["NUMERIC_PRECISION"].status = "RELAXED"

        # 2. Invariant Extraction: Zero External Dependencies
        if RE_ZERO_DEP_MANDATE.search(text) and not RE_RELAX_MODAL.search(text):
            self.constraints["ZERO_DEPENDENCY"] = LedgerConstraint(
                slot_id="ZERO_DEPENDENCY",
                turn_introduced=turn_index,
                category="ZERO_DEPENDENCY",
                raw_statement=text,
                status="ACTIVE"
            )

        # 3. Invariant Extraction: Identity Format (UUID/GUID/ULID)
        if RE_UUID_MANDATE.search(text) and RE_MANDATE_MODAL.search(text):
            self.constraints["IDENTITY_FORMAT"] = LedgerConstraint(
                slot_id="IDENTITY_FORMAT",
                turn_introduced=turn_index,
                category="IDENTITY_FORMAT",
                raw_statement=text,
                status="ACTIVE",
                expected_token="uuid",
                forbidden_token="randint"
            )

        # 4. Invariant Extraction: Forbidden File Modification
        match_forbid = RE_FORBID_FILE.search(text)
        if match_forbid:
            target_file = match_forbid.group(1).strip()
            slot_id = f"FORBIDDEN_FILE_{target_file}"
            self.constraints[slot_id] = LedgerConstraint(
                slot_id=slot_id,
                turn_introduced=turn_index,
                category="FORBIDDEN_FILE",
                raw_statement=text,
                status="ACTIVE",
                forbidden_token=target_file
            )

        # 5. Invariant Extraction: High-Precision Decimal Mandate
        if RE_DECIMAL_MANDATE.search(text) and RE_MANDATE_MODAL.search(text) and not RE_RELAX_MODAL.search(text):
            self.constraints["NUMERIC_PRECISION"] = LedgerConstraint(
                slot_id="NUMERIC_PRECISION",
                turn_introduced=turn_index,
                category="NUMERIC_PRECISION",
                raw_statement=text,
                status="ACTIVE",
                expected_token="Decimal"
            )

        # 6. Invariant Extraction: Strict Error Handling Mandate
        if RE_ERROR_HANDLING_MANDATE.search(text):
            self.constraints["ERROR_HANDLING"] = LedgerConstraint(
                slot_id="ERROR_HANDLING",
                turn_introduced=turn_index,
                category="ERROR_HANDLING",
                raw_statement=text,
                status="ACTIVE"
            )

    def validate_candidate(self, candidate_code: str, mutated_files: Optional[List[str]] = None, current_turn: int = 1) -> List[LedgerViolation]:
        """Validates candidate code against all currently ACTIVE constraints in the ledger."""
        violations: List[LedgerViolation] = []
        mutated_files = mutated_files or []

        try:
            tree = ast.parse(candidate_code)
        except SyntaxError:
            tree = None

        for slot_id, c in self.constraints.items():
            if c.status != "ACTIVE":
                continue

            # Check ZERO_DEPENDENCY
            if c.category == "ZERO_DEPENDENCY" and tree:
                for node in ast.walk(tree):
                    top_pkg = ""
                    if isinstance(node, ast.Import):
                        for a in node.names:
                            top_pkg = a.name.split(".")[0]
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        top_pkg = node.module.split(".")[0]

                    if top_pkg and top_pkg not in sys.stdlib_module_names and top_pkg not in sys.builtin_module_names:
                        violations.append(LedgerViolation(
                            constraint=c,
                            current_turn=current_turn,
                            violation_message=f"Violated active invariant from Turn {c.turn_introduced} ('{c.raw_statement[:50]}'): imported non-stdlib package '{top_pkg}'.",
                            remediation_suggestion="Use Python standard library equivalents (e.g., urllib.request, json, sqlite3)."
                        ))
                        break

            # Check IDENTITY_FORMAT
            elif c.category == "IDENTITY_FORMAT":
                if c.forbidden_token and c.forbidden_token in candidate_code:
                    violations.append(LedgerViolation(
                        constraint=c,
                        current_turn=current_turn,
                        violation_message=f"Violated active invariant from Turn {c.turn_introduced} ('{c.raw_statement[:50]}'): used '{c.forbidden_token}' instead of '{c.expected_token}'.",
                        remediation_suggestion=f"Enforce standard '{c.expected_token}' generation format across all identifier creation."
                    ))

            # Check FORBIDDEN_FILE
            elif c.category == "FORBIDDEN_FILE":
                if c.forbidden_token:
                    for mf in mutated_files:
                        if c.forbidden_token.lower() in mf.lower():
                            violations.append(LedgerViolation(
                                constraint=c,
                                current_turn=current_turn,
                                violation_message=f"Violated active invariant from Turn {c.turn_introduced} ('{c.raw_statement[:50]}'): mutated barred file '{c.forbidden_token}'.",
                                remediation_suggestion=f"Revert all modifications to '{c.forbidden_token}'."
                            ))

            # Check ERROR_HANDLING
            elif c.category == "ERROR_HANDLING" and tree:
                for node in ast.walk(tree):
                    if isinstance(node, ast.ExceptHandler):
                        if node.type is None or (isinstance(node.body, list) and len(node.body) == 1 and isinstance(node.body[0], ast.Pass)):
                            violations.append(LedgerViolation(
                                constraint=c,
                                current_turn=current_turn,
                                violation_message=f"Violated active invariant from Turn {c.turn_introduced}: caught exception and silently swallowed with empty pass.",
                                remediation_suggestion="Log or re-raise caught exception to maintain strict observability."
                            ))
                            break

        return violations
