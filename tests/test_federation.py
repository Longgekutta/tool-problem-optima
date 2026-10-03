#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from pathlib import Path
from engine.tool_federation import ToolFederationCoordinator


class TestToolFederation(unittest.TestCase):
    def setUp(self):
        self.coordinator = ToolFederationCoordinator()

    def test_tool_discovery(self):
        # If sister tools exist in environment, verify resolution
        code_optima = self.coordinator._find_tool_script("tool-code-optima")
        if code_optima is not None:
            self.assertTrue(code_optima.exists())
            self.assertEqual(code_optima.name, "main.py")

        # Verify nonexistent tool is gracefully handled without error
        ghost_tool = self.coordinator._find_tool_script("tool-nonexistent-ghost")
        self.assertIsNone(ghost_tool)

    def test_standalone_isolation(self):
        # Verify that ToolFederationCoordinator runs safely even in a completely isolated directory
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            isolated_coord = ToolFederationCoordinator(workspace_root=Path(td))
            res = isolated_coord.run_syntax_gate("dummy.py")
            self.assertEqual(res.get("status"), "SKIPPED")
            self.assertIn("not found", res.get("reason", ""))

    def test_syntax_gate_invocation(self):
        res = self.coordinator.run_syntax_gate(str(Path(__file__).resolve()))
        self.assertTrue("valid" in res or "status" in res)

    def test_micro_patch_dry_run(self):
        patch = "<<<<<<< SEARCH\n# test comment\n=======\n# modified comment\n>>>>>>> REPLACE"
        res = self.coordinator.apply_micro_patch(str(Path(__file__).resolve()), patch, dry_run=True)
        self.assertTrue(res.get("success") is not None or "status" in res)


if __name__ == "__main__":
    unittest.main()
