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
        micro_patcher = self.coordinator._find_tool_script("tool-micro-patcher")
        self.assertIsNotNone(micro_patcher)
        self.assertTrue(micro_patcher.exists())

        git_ckpt = self.coordinator._find_tool_script("tool-git-checkpoint")
        self.assertIsNotNone(git_ckpt)
        self.assertTrue(git_ckpt.exists())

    def test_syntax_gate_invocation(self):
        res = self.coordinator.run_syntax_gate(str(Path(__file__).resolve()))
        self.assertTrue("valid" in res or "status" in res)

    def test_micro_patch_dry_run(self):
        patch = "<<<<<<< SEARCH\n# test comment\n=======\n# modified comment\n>>>>>>> REPLACE"
        res = self.coordinator.apply_micro_patch(str(Path(__file__).resolve()), patch, dry_run=True)
        self.assertTrue(res.get("success") is not None or "status" in res)


if __name__ == "__main__":
    unittest.main()
