#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from engine.supervisor import SupervisorEngine, SupervisorState


class TestSupervisor(unittest.TestCase):
    def setUp(self):
        self.supervisor = SupervisorEngine()

    def test_supervisor_audit_buggy_code(self):
        bad_code = """
def process(x):
    try:
        if x == 999:
            return 0
        return 1000 // x
    except Exception:
        pass
"""
        report = self.supervisor.audit_code(bad_code, file_path="sample_bad.py")
        self.assertFalse(report.is_sound)
        self.assertEqual(report.status, SupervisorState.REMEDIATION_FEEDBACK)
        self.assertGreater(len(report.ast_findings), 0)
        self.assertIsNotNone(report.tensor_divergence)
        self.assertGreater(report.tensor_divergence.magnitude, 0.0)
        self.assertGreater(len(report.causal_remediation_guide), 0)

    def test_supervisor_audit_clean_code(self):
        good_code = """
def safe_divide(x: int) -> float:
    if x == 0:
        raise ValueError("Division by zero")
    return 1000.0 / x

def test_safe_divide():
    assert safe_divide(2) == 500.0
"""
        report = self.supervisor.audit_code(good_code, file_path="sample_good.py")
        self.assertTrue(report.is_sound)
        self.assertEqual(report.status, SupervisorState.CONVERGED_VERIFIED)
        self.assertEqual(len(report.ast_findings), 0)


if __name__ == "__main__":
    unittest.main()
