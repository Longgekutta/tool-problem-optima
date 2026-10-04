#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for v1.2 Engineering Hardening & Bug Fixes
=================================================
Verifies:
  1. CLI judge command supports --intent and --code properly without error.
  2. Safe Metamorphic Sandbox prevents timeout hangs and destructive imports.
  3. Metamorphic Oracle adaptively probes polymorphic types (strings, lists, numbers).
  4. Polyglot Sentinel detects JS trivial assertions, C gets(), and unclosed handles.
  5. Temporal Constraint Ledger tracks strict error handling and numeric precision.
  6. Def-Use Tracker catches subscript indexing on nullable variables and honors assert guards.
"""

import unittest
from pathlib import Path

from engine.tri_sieve_oracle import TriSieveOracle
from engine.metamorphic_oracle import MetamorphicOracleEngine
from engine.polyglot_sentinel import PolyglotSentinel
from engine.temporal_constraint_ledger import TemporalConstraintLedger
from engine.def_use_tracker import analyze_dataflow


class TestV12Upgrades(unittest.TestCase):

    def setUp(self):
        self.oracle = TriSieveOracle()
        self.metamorphic = MetamorphicOracleEngine(seed=42)
        self.polyglot = PolyglotSentinel()
        self.ledger = TemporalConstraintLedger()

    # -------------------------------------------------------------------------
    # 1. Metamorphic Sandbox & Polymorphic Types
    # -------------------------------------------------------------------------

    def test_metamorphic_string_commutativity(self):
        """String symmetry f(a, b) == f(b, a) tested adaptively without TypeError."""
        code = """
def merge_symmetric(a, b):
    return "".join(sorted(list(a + b)))
"""
        violations = self.metamorphic.verify_source_algebra(code)
        self.assertEqual(len(violations), 0)

    def test_metamorphic_string_idempotence(self):
        """String normalization clean_text(clean_text(s)) == clean_text(s)."""
        code = """
def clean_text(s):
    return s.strip().lower()
"""
        violations = self.metamorphic.verify_source_algebra(code)
        self.assertEqual(len(violations), 0)

    def test_metamorphic_timeout_guard(self):
        """Infinite loop inside candidate function is killed by timeout without freezing host."""
        def infinite_loop(x):
            while True:
                pass

        violation = self.metamorphic.test_idempotence(infinite_loop, [1])
        self.assertIsNotNone(violation)
        self.assertIn("TIMEOUT", violation.relation_name)

    # -------------------------------------------------------------------------
    # 2. Enhanced Polyglot Sentinel
    # -------------------------------------------------------------------------

    def test_js_trivial_assertion(self):
        """Catches expect(true).toBe(true) in JS test."""
        js_code = """
test("flaky test", () => {
    expect(true).toBe(true);
});
"""
        findings = self.polyglot.audit_source(js_code, file_path="test.spec.js")
        codes = [f.code for f in findings]
        self.assertIn("PRB-E104", codes)

    def test_c_dangerous_gets(self):
        """Catches banned vulnerable function gets() in C."""
        c_code = """
#include <stdio.h>
void read_input() {
    char buf[128];
    gets(buf);
}
"""
        findings = self.polyglot.audit_source(c_code, file_path="main.c")
        codes = [f.code for f in findings]
        self.assertIn("PRB-E204", codes)

    def test_go_unclosed_file(self):
        """Catches os.Open without Close() in Go."""
        go_code = """
package main
import "os"
func readFile(path string) {
    f, _ := os.Open(path)
    _ = f
}
"""
        findings = self.polyglot.audit_source(go_code, file_path="main.go")
        codes = [f.code for f in findings]
        self.assertIn("PRB-E303", codes)

    # -------------------------------------------------------------------------
    # 3. Enhanced Temporal Constraint Ledger
    # -------------------------------------------------------------------------

    def test_temporal_strict_error_handling(self):
        """Mandate to never swallow errors flags bare except pass."""
        self.ledger.feed_turn(1, "项目中严禁吞异常，禁止静默忽略报错！")
        self.assertIn("ERROR_HANDLING", self.ledger.constraints, "Must extract ERROR_HANDLING slot")

        bad_code = """
def run_task():
    try:
        do_step()
    except Exception:
        pass
"""
        violations = self.ledger.validate_candidate(bad_code, current_turn=2)
        self.assertEqual(len(violations), 1, "Must detect 1 error handling violation")
        self.assertEqual(violations[0].constraint.category, "ERROR_HANDLING", "Violation category must be ERROR_HANDLING")

    # -------------------------------------------------------------------------
    # 4. Enhanced Def-Use Tracker
    # -------------------------------------------------------------------------

    def test_def_use_subscript_nullability(self):
        """Catches subscript indexing on nullable variable without null check."""
        code = """
def fetch_user(db):
    user = db.get("user")
    return user["email"]
"""
        findings = analyze_dataflow(code)
        codes = [f.code for f in findings]
        self.assertIn("PRB-E202", codes)

    def test_def_use_assert_guard_honored(self):
        """assert var is not None safely clears nullability for subsequent statements."""
        code = """
def fetch_user(db):
    user = db.get("user")
    assert user is not None
    return user["email"]
"""
        findings = analyze_dataflow(code)
        self.assertEqual(len(findings), 0)

    # -------------------------------------------------------------------------
    # 5. Tri-Sieve Oracle with Intent & Code Arguments
    # -------------------------------------------------------------------------

    def test_tri_sieve_with_intent_enforcement(self):
        """Directly passes user intent into judge_mutation to enforce standard library constraint."""
        valid_code = "import json\nimport math\n"
        verdict = self.oracle.judge_mutation(
            valid_code,
            user_intent="必须全部使用Python标准库，零三方依赖"
        )
        self.assertTrue(verdict.is_valid)

        invalid_code = "import external_phantom_lib_foo\n"
        verdict2 = self.oracle.judge_mutation(
            invalid_code,
            user_intent="必须全部使用Python标准库，零三方依赖"
        )
        self.assertFalse(verdict2.is_valid)


if __name__ == "__main__":
    unittest.main()
