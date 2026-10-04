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

    def test_detect_weak_assertions_only(self):
        """PRB-E105: Detect test functions relying entirely on weak assertions (is not None, len > 0, isinstance)."""
        source = """
def test_user_query():
    res = {"name": "alice"}
    assert res is not None
    assert len(res) > 0
    assert isinstance(res, dict)
"""
        findings = audit_source_code(source, file_path="test_users.py")
        codes = [f.code for f in findings]
        self.assertIn("PRB-E105", codes)
        self.assertTrue(any("weak assertion" in f.name.lower() or "weak" in f.message.lower() for f in findings))

    def test_sharp_assertion_alongside_weak_passes(self):
        """Sharp assertion alongside weak guard must pass without false alarm."""
        source = """
def test_valid_sharp():
    res = {"name": "alice", "score": 98}
    assert res is not None
    assert res["name"] == "alice"
"""
        findings = audit_source_code(source, file_path="test_users.py")
        codes = [f.code for f in findings]
        self.assertNotIn("PRB-E105", codes)

    def test_detect_call_contract_drift_mismatch(self):
        """PRB-E109: Detect call-site contract drift (missing required argument / unknown kwarg)."""
        source = """
def process_order(order_id, user_id, amount):
    return order_id + user_id + amount

def run():
    process_order(1, 2)  # Missing amount!
"""
        findings = audit_source_code(source)
        codes = [f.code for f in findings]
        self.assertIn("PRB-E109", codes)

    def test_detect_version_contract_drift(self):
        """PRB-E109: Detect breaking changes between versions (e.g. deleting public parameter)."""
        v1 = """
def format_output(data, indent=2, pretty=True):
    return str(data)
"""
        v2 = """
def format_output(data):  # Removed indent and pretty!
    return str(data)
"""
        findings = audit_source_code(v2, previous_source=v1)
        codes = [f.code for f in findings]
        self.assertIn("PRB-E109", codes)



if __name__ == "__main__":
    unittest.main()
