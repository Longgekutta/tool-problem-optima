#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for TriSieveOracle.
"""

import unittest
from engine.tri_sieve_oracle import TriSieveOracle, TriSieveVerdict
from engine.context_distiller_bridge import TriAnchorSlice


class TestTriSieveOracle(unittest.TestCase):

    def setUp(self):
        self.oracle = TriSieveOracle()

    def test_sieve1_catches_tautological_assert(self):
        buggy_code = """
def test_something():
    assert True
"""
        verdict = self.oracle.judge_mutation(buggy_code)
        self.assertFalse(verdict.is_valid)
        self.assertFalse(verdict.sieve1_pass)
        self.assertTrue(any("PRB-E104" in f for f in verdict.sieve1_findings))
        self.assertEqual(verdict.final_status, "REJECTED_ROLLED_BACK")

    def test_sieve1_catches_bare_except(self):
        buggy_code = """
def risky():
    try:
        1 / 0
    except:
        pass
"""
        verdict = self.oracle.judge_mutation(buggy_code)
        self.assertFalse(verdict.is_valid)
        self.assertFalse(verdict.sieve1_pass)
        self.assertTrue(any("PRB-E108" in f for f in verdict.sieve1_findings))

    def test_sieve2_metamorphic_algebra_pass(self):
        clean_code = """
def add_symmetric(a, b):
    return a + b
"""
        verdict = self.oracle.judge_mutation(clean_code)
        self.assertTrue(verdict.sieve1_pass)
        self.assertTrue(verdict.sieve2_pass)
        self.assertTrue(verdict.is_valid)
        self.assertEqual(verdict.final_status, "COMMITTED")

    def test_sieve3_catches_ghost_tooling(self):
        clean_code = """
def compute(x):
    return x * 2
"""
        # AI CoT claims tests passed, but action_calls has no test/audit tool!
        fake_slice = TriAnchorSlice(
            user_intent="Fix compute function",
            reasoning_claims="I ran the unit tests and verified all tests pass cleanly.",
            action_calls=[{"name": "write_to_file", "args": {"TargetFile": "compute.py"}}],
            action_results=[],
            mutated_files=["compute.py"],
            raw_turn_span=2,
            compression_ratio=50.0
        )

        verdict = self.oracle.judge_mutation(clean_code, causal_slice=fake_slice)
        self.assertFalse(verdict.is_valid)
        self.assertTrue(verdict.sieve1_pass)
        self.assertTrue(verdict.sieve2_pass)
        self.assertFalse(verdict.sieve3_pass)
        self.assertTrue(any("PRB-E107" in d for d in verdict.sieve3_discrepancies))

    def test_sieve3_passes_honest_verified_action(self):
        clean_code = """
def compute(x):
    return x * 2
"""
        # Honest AI CoT with actual test command in tool_calls
        honest_slice = TriAnchorSlice(
            user_intent="Fix compute function",
            reasoning_claims="I ran the unit tests to confirm multiplication holds.",
            action_calls=[
                {"name": "run_command", "args": {"CommandLine": "python -m unittest test_compute.py"}}
            ],
            action_results=[{"exit_code": 0}],
            mutated_files=["compute.py"],
            raw_turn_span=2,
            compression_ratio=50.0
        )

        verdict = self.oracle.judge_mutation(clean_code, causal_slice=honest_slice)
        self.assertTrue(verdict.is_valid)
        self.assertTrue(verdict.sieve3_pass)
        self.assertEqual(verdict.final_status, "COMMITTED")


if __name__ == "__main__":
    unittest.main()
