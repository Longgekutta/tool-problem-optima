#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Def-Use Dataflow Tracking, Temporal Constraint Ledger, and Polyglot Sentinel
======================================================================================
Verifies that:
  1. Def-Use dataflow correctly catches inter-statement nullability (PRB-E202) and resource leaks (PRB-E303).
  2. Temporal Constraint Ledger tracks multi-turn invariants across turns and honors relaxations.
  3. Polyglot Sentinel detects pathologies across JS/TS, C/C++, and Go.
"""

import unittest
from engine.def_use_tracker import analyze_dataflow
from engine.temporal_constraint_ledger import TemporalConstraintLedger
from engine.polyglot_sentinel import PolyglotSentinel
from engine.tri_sieve_oracle import TriSieveOracle


class TestDefUseAndPolyglot(unittest.TestCase):
    def setUp(self):
        self.oracle = TriSieveOracle()
        self.polyglot = PolyglotSentinel()
        self.ledger = TemporalConstraintLedger()

    # =========================================================================
    # 1. Def-Use Dataflow Tracking
    # =========================================================================

    def test_def_use_nullability_violation(self):
        """Inter-statement null dereference without check."""
        code = """
def process(data):
    val = data.get("user")
    # multiple statements in between
    x = 10
    y = 20
    return val.strip()
"""
        findings = analyze_dataflow(code)
        codes = [f.code for f in findings]
        self.assertIn("PRB-E202", codes)

    def test_def_use_nullability_guarded_pass(self):
        """Inter-statement null dereference safely guarded."""
        code = """
def process(data):
    val = data.get("user")
    if val is not None:
        return val.strip()
    return ""
"""
        findings = analyze_dataflow(code)
        self.assertEqual(len(findings), 0)

    def test_def_use_unmanaged_resource_leak(self):
        """Raw open assigned to variable without close."""
        code = """
def read_data(path):
    f = open(path)
    data = f.read()
    return data
"""
        findings = analyze_dataflow(code)
        codes = [f.code for f in findings]
        self.assertIn("PRB-E303", codes)

    def test_def_use_resource_closed_pass(self):
        """Raw open explicitly closed."""
        code = """
def read_data(path):
    f = open(path)
    data = f.read()
    f.close()
    return data
"""
        findings = analyze_dataflow(code)
        self.assertEqual(len(findings), 0)

    # =========================================================================
    # 2. Multi-Turn Temporal Constraint Ledger
    # =========================================================================

    def test_temporal_ledger_multi_turn_retention(self):
        """Constraint established in Turn 1 must be honored in Turn 20."""
        # Turn 1: user mandates zero dependencies
        self.ledger.feed_turn(1, "We require zero external dependencies and pure standard library.")
        
        # Turn 20: AI generates code importing requests
        violations = self.ledger.validate_candidate("import requests\n", current_turn=20)
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].constraint.category, "ZERO_DEPENDENCY")

    def test_temporal_ledger_relaxation(self):
        """Constraint relaxed in Turn 5 permits subsequent usage."""
        self.ledger.feed_turn(1, "We require zero external dependencies.")
        # Turn 5 relaxes requirement
        self.ledger.feed_turn(5, "You can now use requests for network calls.")
        
        # Turn 6 generates code importing requests -> Allowed!
        violations = self.ledger.validate_candidate("import requests\n", current_turn=6)
        self.assertEqual(len(violations), 0)

    def test_temporal_ledger_generalized_mandates(self):
        """Generalized constraint phrasing without brittle exact keyword matching."""
        ledger = TemporalConstraintLedger()
        # Chinese phrasing without standard keyword:
        ledger.feed_turn(1, "这个项目禁止引入任何第三方库，只能用纯内置模块！")
        self.assertIn("ZERO_DEPENDENCY", ledger.constraints)
        self.assertEqual(ledger.constraints["ZERO_DEPENDENCY"].status, "ACTIVE")

        violations = ledger.validate_candidate("import httpx\n", current_turn=10)
        self.assertEqual(len(violations), 1)

        # Chinese relaxation:
        ledger.feed_turn(11, "解除第三方依赖限制，现在可以使用外部网络包了。")
        self.assertEqual(ledger.constraints["ZERO_DEPENDENCY"].status, "RELAXED")
        violations_after = ledger.validate_candidate("import httpx\n", current_turn=12)
        self.assertEqual(len(violations_after), 0)


    # =========================================================================
    # 3. Polyglot Multi-Language Sentinel
    # =========================================================================

    def test_javascript_pathologies(self):
        """JavaScript empty catch and float equality."""
        js_code = """
function calculate(r) {
    if (r === 0.1) {
        try {
            doSomething();
        } catch (e) {
        }
    }
}
"""
        findings = self.polyglot.audit_source(js_code, file_path="solver.js")
        codes = [f.code for f in findings]
        self.assertIn("PRB-E108", codes)  # Empty catch
        self.assertIn("PRB-E203", codes)  # Float equality

    def test_cpp_pathologies(self):
        """C++ TOCTOU race condition."""
        cpp_code = """
#include <stdio.h>
#include <unistd.h>
void process_file(const char* p) {
    if (access(p, R_OK) == 0) {
        FILE* f = fopen(p, "r");
    }
}
"""
        findings = self.polyglot.audit_source(cpp_code, file_path="loader.cpp")
        codes = [f.code for f in findings]
        self.assertIn("PRB-E301", codes)

    def test_go_pathologies(self):
        """Go blank error discard and unbounded goroutine in loop."""
        go_code = """
package main
func handle(items []string) {
    for _, item := range items {
        go func() {
            _ = doWork(item)
        }()
    }
}
"""
        findings = self.polyglot.audit_source(go_code, file_path="worker.go")
        codes = [f.code for f in findings]
        self.assertIn("PRB-E304", codes)  # Unbounded goroutine in loop


if __name__ == "__main__":
    unittest.main()
