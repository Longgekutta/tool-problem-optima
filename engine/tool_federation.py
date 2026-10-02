#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool Federation: Multi-Tool Meta-Orchestrator for GitHub Tool Ecosystem
=======================================================================
Coordinates specialized industrial mother machines in D:/github:
  - tool-code-optima: Code size bloat, dependency pruner, cognitive complexity
  - tool-syntax-gate: Sub-millisecond AST pre-flight verification
  - tool-tdd-runner: Sandboxed deterministic test runner
  - tool-omniscout-radar: Autonomous technology and benchmark radar

Synthesizes external tool findings with Problemology Tensor diagnostics.
"""

import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, Any, Optional


class ToolFederationCoordinator:
    def __init__(self, workspace_root: Optional[Path] = None):
        if workspace_root is None:
            # Default to D:/github or parent directory
            self.workspace_root = Path("D:/github").resolve()
            if not self.workspace_root.exists():
                self.workspace_root = Path(__file__).resolve().parent.parent.parent
        else:
            self.workspace_root = workspace_root

    def _find_tool_script(self, tool_name: str) -> Optional[Path]:
        """Locates the main.py or run.ps1 of a sister tool."""
        target = self.workspace_root / tool_name / "main.py"
        if target.exists():
            return target
        return None

    def run_syntax_gate(self, target_path: str) -> Dict[str, Any]:
        """Invokes tool-syntax-gate for instant AST validation."""
        script = self._find_tool_script("tool-syntax-gate")
        if not script:
            return {"status": "SKIPPED", "reason": "tool-syntax-gate not found"}

        cmd = [sys.executable, str(script), "run", "--path", str(target_path), "--json"]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if res.returncode == 0:
                try:
                    return json.loads(res.stdout)
                except Exception:
                    return {"status": "PASS", "raw": res.stdout.strip()}
            return {"status": "FAIL", "errors": res.stderr.strip() or res.stdout.strip()}
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

    def run_code_optima_audit(self, target_path: str) -> Dict[str, Any]:
        """Invokes tool-code-optima for size bloat and complexity audit."""
        script = self._find_tool_script("tool-code-optima")
        if not script:
            return {"status": "SKIPPED", "reason": "tool-code-optima not found"}

        cmd = [sys.executable, str(script), "audit", str(target_path), "--json"]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if res.stdout.strip():
                try:
                    return json.loads(res.stdout)
                except Exception:
                    return {"status": "COMPLETE", "raw": res.stdout.strip()[:500]}
            return {"status": "COMPLETE", "exit_code": res.returncode}
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

    def run_tdd_suite(self, target_dir: str, test_cmd: str = "python -m unittest discover -s tests") -> Dict[str, Any]:
        """Invokes tool-tdd-runner for sandboxed test execution."""
        script = self._find_tool_script("tool-tdd-runner")
        if not script:
            return {"status": "SKIPPED", "reason": "tool-tdd-runner not found"}

        cmd = [sys.executable, str(script), "run", "--cwd", str(target_dir), "--cmd", test_cmd, "--json"]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
            if res.stdout.strip():
                try:
                    return json.loads(res.stdout)
                except Exception:
                    return {"status": "COMPLETE", "raw": res.stdout.strip()}
            return {"status": "COMPLETE", "exit_code": res.returncode}
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

    def probe_omniscout(self, query: str) -> Dict[str, Any]:
        """Invokes tool-omniscout-radar for state-of-the-art benchmark exploration."""
        script = self._find_tool_script("tool-omniscout-radar")
        if not script:
            return {"status": "SKIPPED", "reason": "tool-omniscout-radar not found"}

        cmd = [sys.executable, str(script), "radar", query, "--concise", "--json"]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if res.stdout.strip():
                try:
                    return json.loads(res.stdout)
                except Exception:
                    return {"status": "COMPLETE", "raw": res.stdout.strip()[:500]}
            return {"status": "COMPLETE"}
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

    def federated_audit(self, target_path: str) -> Dict[str, Any]:
        """Coordinates all available productivity tools to evaluate target code."""
        return {
            "target": str(target_path),
            "syntax_gate": self.run_syntax_gate(target_path),
            "code_optima": self.run_code_optima_audit(target_path),
            "tdd_runner": self.run_tdd_suite(target_path)
        }
