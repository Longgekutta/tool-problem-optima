#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from engine.ast_interceptor import audit_source_code


class TestASTInterceptor(unittest.TestCase):
    def test_detect_patch_overfitting(self):
        source = """
def solve_issue(x, y):
    if x == 42 and y == "bug":
        return 100
    return x + y
"""
        findings = audit_source_code(source)
        codes = [f.code for f in findings]
        self.assertIn("PRB-E101", codes)

    def test_detect_tautological_verification(self):
        source = """
def test_something():
    assert True
    assert 42 == 42
"""
        findings = audit_source_code(source)
        codes = [f.code for f in findings]
        self.assertIn("PRB-E104", codes)

    def test_detect_zero_assertion(self):
        source = """
def test_dummy_empty():
    print("Just running without assertions to inflate coverage")
"""
        findings = audit_source_code(source)
        codes = [f.code for f in findings]
        self.assertIn("PRB-E105", codes)

    def test_detect_bare_except(self):
        source = """
def fetch_data():
    try:
        do_work()
    except Exception:
        pass
"""
        findings = audit_source_code(source)
        codes = [f.code for f in findings]
        self.assertIn("PRB-E108", codes)

    def test_clean_code_passes(self):
        source = """
def add(a: int, b: int) -> int:
    return a + b

def test_add():
    assert add(1, 2) == 3
"""
        findings = audit_source_code(source)
        self.assertEqual(len(findings), 0)


if __name__ == "__main__":
    unittest.main()
