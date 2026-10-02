#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from pathlib import Path
from engine.tool_federation import ToolFederationCoordinator


class TestToolFederation(unittest.TestCase):
    def setUp(self):
        self.coordinator = ToolFederationCoordinator()

    def test_tool_discovery(self):
        # Verify sister tool discovery in D:/github
        code_optima = self.coordinator._find_tool_script("tool-code-optima")
        self.assertIsNotNone(code_optima)
        self.assertTrue(code_optima.exists())

        syntax_gate = self.coordinator._find_tool_script("tool-syntax-gate")
        self.assertIsNotNone(syntax_gate)
        self.assertTrue(syntax_gate.exists())

    def test_syntax_gate_invocation(self):
        res = self.coordinator.run_syntax_gate(str(Path(__file__).resolve()))
        self.assertTrue("valid" in res or "status" in res)


if __name__ == "__main__":
    unittest.main()
