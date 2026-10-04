#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for v1.3 Daily Project Construction & AI Coding Pragmatic Guards:
  1. Mutable default arguments (def f(x=[], y={})) [PRB-E109]
  2. Unawaited coroutines (calling async def without await) [PRB-E109]
  3. Tuple assertion trap (assert (x == 1, "msg")) [PRB-E104]
  4. Literal identity comparison (is "string" / is 42) [PRB-E202]
  5. Fencepost range off-by-one (range(len(x) + 1)) [PRB-E201]
  6. Bare exception with continue (except: continue) [PRB-E108]
"""

import unittest
from engine.ast_interceptor import audit_source_code


class TestV13PragmaticGuards(unittest.TestCase):
    def test_mutable_default_arguments_caught(self):
        """Detects mutable default arguments in functions (Flake8 B006 / Ruff B006)."""
        code = "def process_data(items=[], config={}):\n    items.append(1)\n    return items\n"
        findings = audit_source_code(code)
        codes = [f.code for f in findings]
        self.assertIn("PRB-E109", codes, "Must flag mutable default arguments with PRB-E109")
        names = [f.name for f in findings]
        self.assertTrue(any("Mutable Default Argument" in n for n in names), "Finding name must specify mutable default argument")

    def test_clean_default_arguments_pass(self):
        """Passes when default arguments are immutable singletons or scalars."""
        code = "def process_data(items=None, timeout=30, debug=False):\n    if items is None:\n        items = []\n    return items\n"
        findings = audit_source_code(code)
        self.assertEqual(len(findings), 0, f"Clean defaults must pass with 0 findings, got: {findings}")

    def test_unawaited_coroutine_caught(self):
        """Flags calls to async functions in expression statements without await."""
        code = "async def sync_remote():\n    pass\n\ndef execute():\n    sync_remote()\n"
        findings = audit_source_code(code)
        codes = [f.code for f in findings]
        self.assertIn("PRB-E109", codes, "Must flag unawaited coroutine call with PRB-E109")
        names = [f.name for f in findings]
        self.assertTrue(any("Unawaited Coroutine" in n for n in names), "Finding name must specify unawaited coroutine")

    def test_properly_awaited_coroutine_passes(self):
        """Passes when async function is properly awaited."""
        code = "async def sync_remote():\n    pass\n\nasync def execute():\n    await sync_remote()\n"
        findings = audit_source_code(code)
        self.assertEqual(len(findings), 0, f"Properly awaited async call must pass with 0 findings, got: {findings}")

    def test_tuple_assertion_trap_caught(self):
        """Flags non-empty tuple assertion (assert (cond, msg)) which is always truthy."""
        code = "def test_logic():\n    assert (1 == 2, 'Value mismatch')\n"
        findings = audit_source_code(code, file_path="test_sample.py")
        codes = [f.code for f in findings]
        self.assertIn("PRB-E104", codes, "Must flag tuple assertion trap with PRB-E104")
        names = [f.name for f in findings]
        self.assertTrue(any("Tuple Assertion Trap" in n for n in names), "Finding name must specify tuple assertion trap")

    def test_clean_assertion_with_message_passes(self):
        """Passes when assertion uses standard comma separation: assert cond, msg."""
        code = "def test_logic():\n    x = 10\n    assert x == 10, 'Expected 10'\n"
        findings = audit_source_code(code, file_path="test_sample.py")
        self.assertEqual(len(findings), 0, f"Clean assert cond, msg must pass with 0 findings, got: {findings}")

    def test_literal_identity_comparison_caught(self):
        """Flags comparing literals using 'is'/'is not' (SyntaxWarning / Ruff F632)."""
        code = "def check_name(name):\n    if name is 'admin':\n        return True\n    return False\n"
        findings = audit_source_code(code)
        codes = [f.code for f in findings]
        self.assertIn("PRB-E202", codes, "Must flag 'is' comparison with string literal with PRB-E202")

    def test_singleton_identity_comparison_passes(self):
        """Passes when 'is' is used for None, True, False singletons."""
        code = "def check_empty(val):\n    if val is None or val is True:\n        return True\n    return False\n"
        findings = audit_source_code(code)
        self.assertEqual(len(findings), 0, f"Singleton identity comparisons must pass, got: {findings}")

    def test_range_len_plus_one_caught(self):
        """Flags range(len(...) + 1) fencepost off-by-one index error."""
        code = "def iterate(arr):\n    for i in range(len(arr) + 1):\n        print(arr[i])\n"
        findings = audit_source_code(code)
        codes = [f.code for f in findings]
        self.assertIn("PRB-E201", codes, "Must flag range(len(...) + 1) with PRB-E201")

    def test_standard_range_len_passes(self):
        """Passes when range(len(...)) is used within sequence bounds."""
        code = "def iterate(arr):\n    for i in range(len(arr)):\n        print(arr[i])\n"
        findings = audit_source_code(code)
        self.assertEqual(len(findings), 0, f"Standard range(len(...)) must pass with 0 findings, got: {findings}")

    def test_bare_except_continue_caught(self):
        """Flags bare except followed by continue."""
        code = "def loop_process(items):\n    for item in items:\n        try:\n            item.process()\n        except:\n            continue\n"
        findings = audit_source_code(code)
        codes = [f.code for f in findings]
        self.assertIn("PRB-E108", codes, "Must flag bare except with continue with PRB-E108")

    def test_alias_bound_mutable_default_caught_via_symbol_resolution(self):
        """Catches mutable default argument bound through an alias variable defined earlier."""
        code = "DEFAULT_REGISTRY = []\ndef register_handler(h, registry=DEFAULT_REGISTRY):\n    registry.append(h)\n"
        findings = audit_source_code(code)
        codes = [f.code for f in findings]
        self.assertIn("PRB-E109", codes, "Must flag alias-bound mutable default argument with PRB-E109")
        messages = [f.message for f in findings]
        self.assertTrue(any("bound via alias 'DEFAULT_REGISTRY'" in m for m in messages), "Message must detail the alias binding")

    def test_alias_bound_literal_comparison_caught_via_symbol_resolution(self):
        """Catches 'is' comparison with a scalar literal defined earlier as a constant."""
        code = "ADMIN_ROLE = 'administrator'\ndef check_role(role):\n    if role is ADMIN_ROLE:\n        return True\n    return False\n"
        findings = audit_source_code(code)
        codes = [f.code for f in findings]
        self.assertIn("PRB-E202", codes, "Must flag alias-bound literal identity comparison with PRB-E202")

    def test_unawaited_stdlib_asyncio_sleep_caught(self):
        """Catches unawaited stdlib async calls like asyncio.sleep()."""
        code = "import asyncio\ndef run_worker():\n    asyncio.sleep(1)\n"
        findings = audit_source_code(code)
        codes = [f.code for f in findings]
        self.assertIn("PRB-E109", codes, "Must flag unawaited asyncio.sleep with PRB-E109")


if __name__ == "__main__":
    unittest.main()
