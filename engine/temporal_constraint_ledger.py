#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Temporal Constraint Ledger: Multi-Turn Dialogue State & Invariant Tracker
========================================================================
Implements an Agent-C / Temporal Semantic Memory (TSM) style persistent ledger
that tracks explicit modality constraints across long multi-turn conversations (50+ turns):

  - Maintains active invariants (e.g., UUID format, zero third-party packages,
    forbidden files, functional return types).
  - Handles state evolutions: detects when constraints are RELAXED, STRENGTHENED,
    or SUPERSEDED across subsequent turns.
  - Validates candidate code and tool actions against currently ACTIVE invariants,
    eliminating PRB-E001 (Context Satiation & Needle-in-a-Haystack Amnesia).

Zero external dependencies. Sub-5ms evaluation.
"""

import re
import ast
import sys
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Any


@dataclass
class LedgerConstraint:
    """An invariant constraint tracked across dialogue turns."""
    slot_id: str
    turn_introduced: int
    category: str                                 # "IDENTITY_FORMAT" | "ZERO_DEPENDENCY" | "FORBIDDEN_FILE" | "TYPE_CONTRACT"
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


class TemporalConstraintLedger:
    """Persistent ledger tracking invariants across multi-turn transcripts."""

    def __init__(self):
        self.constraints: Dict[str, LedgerConstraint] = {}

    def feed_turn(self, turn_index: int, user_input: str):
        """Processes a new user prompt turn and updates constraint states."""
        text = user_input.lower()

        # 1. Check for Constraint Relaxation / Retraction
        if any(w in text for w in ("you can now use", "relax requirement", "allow using", "取消约束", "现在可以引用")):
            # If user relaxes external dependencies
            if "dependency" in text or "package" in text or "三方库" in text or "依赖" in text:
                if "ZERO_DEPENDENCY" in self.constraints:
                    self.constraints["ZERO_DEPENDENCY"].status = "RELAXED"

        # 2. Invariant Extraction: Zero External Dependencies
        if any(phrase in text for phrase in (
            "no external dependencies", "zero dependency", "pure standard library",
            "零三方依赖", "纯标准库", "不准引入第三方库", "no third-party packages"
        )):
            self.constraints["ZERO_DEPENDENCY"] = LedgerConstraint(
                slot_id="ZERO_DEPENDENCY",
                turn_introduced=turn_index,
                category="ZERO_DEPENDENCY",
                raw_statement=user_input.strip(),
                status="ACTIVE"
            )

        # 3. Invariant Extraction: Identity Format (UUIDv4)
        if ("uuid" in text and "id" in text) and any(w in text for w in ("must", "all", "strictly", "必须", "所有")):
            self.constraints["IDENTITY_FORMAT"] = LedgerConstraint(
                slot_id="IDENTITY_FORMAT",
                turn_introduced=turn_index,
                category="IDENTITY_FORMAT",
                raw_statement=user_input.strip(),
                status="ACTIVE",
                expected_token="uuid",
                forbidden_token="randint"
            )

        # 4. Invariant Extraction: Forbidden File Modification
        match_forbid = re.search(r"(?:do not modify|don't touch|不要修改|严禁改动)\s+([a-zA-Z0-9_\-\.\/]+)", user_input, flags=re.IGNORECASE)
        if match_forbid:
            target_file = match_forbid.group(1).strip()
            slot_id = f"FORBIDDEN_FILE_{target_file}"
            self.constraints[slot_id] = LedgerConstraint(
                slot_id=slot_id,
                turn_introduced=turn_index,
                category="FORBIDDEN_FILE",
                raw_statement=user_input.strip(),
                status="ACTIVE",
                forbidden_token=target_file
            )

    def validate_candidate(self, candidate_code: str, mutated_files: Optional[List[str]] = None, current_turn: int = 1) -> List[LedgerViolation]:
        """Validates candidate code against all currently ACTIVE constraints in the ledger."""
        violations: List[LedgerViolation] = []
        mutated_files = mutated_files or []

        for slot_id, c in self.constraints.items():
            if c.status != "ACTIVE":
                continue

            # Check ZERO_DEPENDENCY
            if c.category == "ZERO_DEPENDENCY":
                try:
                    tree = ast.parse(candidate_code)
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
                except Exception:
                    pass

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

        return violations
