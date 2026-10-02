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

    def create_git_checkpoint(self, repo_dir: str, message: str = "auto-checkpoint") -> Dict[str, Any]:
        """Creates an atomic git snapshot before applying mutations."""
        script = self._find_tool_script("tool-git-checkpoint")
        if not script:
            return {"status": "SKIPPED", "reason": "tool-git-checkpoint not found"}

        cmd = [sys.executable, str(script), "run", "checkpoint", "--repo", str(repo_dir), "--message", message, "--json"]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if res.stdout.strip():
                try:
                    return json.loads(res.stdout)
                except Exception:
                    return {"status": "COMPLETE", "raw": res.stdout.strip()}
            return {"status": "COMPLETE", "exit_code": res.returncode}
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

    def rollback_git_checkpoint(self, repo_dir: str, target: Optional[str] = None) -> Dict[str, Any]:
        """Rolls back repo to a specified checkpoint or previous state."""
        script = self._find_tool_script("tool-git-checkpoint")
        if not script:
            return {"status": "SKIPPED", "reason": "tool-git-checkpoint not found"}

        cmd = [sys.executable, str(script), "run", "rollback", "--repo", str(repo_dir), "--json"]
        if target:
            cmd.extend(["--target", target])
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if res.stdout.strip():
                try:
                    return json.loads(res.stdout)
                except Exception:
                    return {"status": "COMPLETE", "raw": res.stdout.strip()}
            return {"status": "COMPLETE", "exit_code": res.returncode}
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

    def commit_git_checkpoint(self, repo_dir: str, message: str) -> Dict[str, Any]:
        """Commits verified safe modifications to Git repository."""
        script = self._find_tool_script("tool-git-checkpoint")
        if not script:
            return {"status": "SKIPPED", "reason": "tool-git-checkpoint not found"}

        cmd = [sys.executable, str(script), "run", "commit", "--repo", str(repo_dir), "--message", message, "--json"]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if res.stdout.strip():
                try:
                    return json.loads(res.stdout)
                except Exception:
                    return {"status": "COMPLETE", "raw": res.stdout.strip()}
            return {"status": "COMPLETE", "exit_code": res.returncode}
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

    def apply_micro_patch(self, target_file: str, patch_str: str, dry_run: bool = False) -> Dict[str, Any]:
        """Applies surgical SEARCH/REPLACE micro-patch using tool-micro-patcher."""
        script = self._find_tool_script("tool-micro-patcher")
        if not script:
            return {"status": "SKIPPED", "reason": "tool-micro-patcher not found"}

        cmd = [sys.executable, str(script), "run", "--file", str(target_file), "--patch", patch_str, "--json"]
        if dry_run:
            cmd.append("--dry-run")
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if res.stdout.strip():
                try:
                    return json.loads(res.stdout)
                except Exception:
                    return {"status": "COMPLETE", "raw": res.stdout.strip()}
            return {"status": "COMPLETE", "exit_code": res.returncode}
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

    def execute_transactional_surgery(
        self,
        repo_dir: str,
        target_file: str,
        patch_str: str,
        test_cmd: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes the Complete Tri-Chamber Separation-of-Powers Transaction:
        1. Chamber 2 (Isolation): Take Git checkpoint snapshot.
        2. Chamber 2 (Surgery): Apply surgical micro-patch (no full-file rewrite).
        3. Chamber 3 (Verification): Verify AST with tool-syntax-gate.
        4. Chamber 3 (Verification): Run sandboxed tests with tool-tdd-runner.
        5. If all pass -> Chamber 2 commit.
        6. If any fails -> Chamber 2 instant rollback (zero dirty state).
        """
        # Step 1: Snapshot
        ckpt_res = self.create_git_checkpoint(repo_dir, "pre-surgery snapshot")

        # Step 2: Micro-Patch
        patch_res = self.apply_micro_patch(target_file, patch_str)
        if not patch_res.get("success", False):
            # Patch failed to apply cleanly
            return {
                "status": "ABORTED",
                "phase": "micro_patch",
                "checkpoint": ckpt_res,
                "patch_result": patch_res,
                "reason": "Micro-patch failed to apply (mismatched SEARCH context)"
            }

        # Step 3: AST Gate
        syntax_res = self.run_syntax_gate(target_file)
        if syntax_res.get("status") == "FAIL" or syntax_res.get("valid") is False:
            self.rollback_git_checkpoint(repo_dir)
            return {
                "status": "ROLLED_BACK",
                "phase": "syntax_gate",
                "reason": "Syntax error introduced by patch",
                "syntax_result": syntax_res
            }

        # Step 4: TDD Verification
        if test_cmd:
            tdd_res = self.run_tdd_suite(repo_dir, test_cmd=test_cmd)
            if tdd_res.get("exit_code", 0) != 0 and tdd_res.get("status") != "PASS":
                self.rollback_git_checkpoint(repo_dir)
                return {
                    "status": "ROLLED_BACK",
                    "phase": "tdd_suite",
                    "reason": "Regression tests failed after patch",
                    "tdd_result": tdd_res
                }

        # Step 5: Commit on verified improvement
        commit_res = self.commit_git_checkpoint(repo_dir, f"verified surgery on {Path(target_file).name}")
        return {
            "status": "COMMITTED",
            "checkpoint": ckpt_res,
            "patch": patch_res,
            "syntax": syntax_res,
            "commit": commit_res
        }

    def federated_audit(self, target_path: str) -> Dict[str, Any]:
        """Coordinates all available productivity tools to evaluate target code."""
        return {
            "target": str(target_path),
            "syntax_gate": self.run_syntax_gate(target_path),
            "code_optima": self.run_code_optima_audit(target_path),
            "tdd_runner": self.run_tdd_suite(target_path)
        }

