#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnostic Renderer: Miette & Rust-Grade Terminal UI for Problem Pathology
==========================================================================
Produces beautiful, high-density, informative diagnostic views:
  - Precise source code line highlights with caret squiggles (^^^^)
  - Color-coded severity tiers (Fatal / Error / Warning / Note)
  - Scientific authority citations and first-principles causal cards
  - Real-time ASCII radar chart projection of the Problemology Tensor
"""

import sys
from typing import List, Optional, Any
from .ast_interceptor import DiagnosticFinding
try:
    from core.pathology_catalog import get_catalog_entry
except (ImportError, ValueError):
    from ..core.pathology_catalog import get_catalog_entry


# ANSI Color Codes (Self-Contained, Zero External Dependencies)
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BG_DARK = "\033[48;5;236m"


class DiagnosticRenderer:
    def __init__(self, use_color: bool = True):
        self.use_color = use_color and sys.stdout.isatty()

    def _c(self, text: str, color: str) -> str:
        if not self.use_color:
            return text
        return f"{color}{text}{RESET}"

    def render_finding(self, finding: DiagnosticFinding, source_lines: Optional[List[str]] = None) -> str:
        """Renders an individual diagnostic finding with source highlight and radar."""
        entry = get_catalog_entry(finding.code)
        lines = []

        # Header Box
        header = f"[{finding.code}] {finding.name}"
        lines.append(self._c(f"┌── {header} " + "─" * max(0, 68 - len(header)) + "┐", RED + BOLD))
        lines.append(self._c(f"│  File: {finding.file_path}:{finding.line_number}:{finding.column + 1}", CYAN))
        lines.append(self._c(f"│  Defect: {finding.message}", WHITE + BOLD))

        # Source code snippet context
        if source_lines and 1 <= finding.line_number <= len(source_lines):
            lines.append(self._c("│  ", DIM))
            line_idx = finding.line_number - 1
            code_line = source_lines[line_idx]
            ln_str = f"{finding.line_number:4d} | "
            lines.append(self._c(f"│  {ln_str}", DIM) + self._c(code_line, WHITE))
            
            # Squiggle pointer
            indent = " " * (len(ln_str) + finding.column)
            squiggle_len = max(3, len(finding.snippet.strip()))
            lines.append(self._c(f"│  {indent}" + "^" * squiggle_len + f" [Violation here]", RED + BOLD))
            lines.append(self._c("│  ", DIM))

        # Scientific & First-Principles Attribution
        if entry:
            lines.append(self._c(f"│  📚 学术领域: {entry.domain}", YELLOW))
            lines.append(self._c(f"│  🏛️ 权威出处: {entry.authorities}", DIM))
            lines.append(self._c(f"│  🧬 第一性成因: {entry.first_principles_cause}", MAGENTA))
            lines.append(self._c(f"│  🛡️ 修复神谕: {entry.remediation_oracle}", GREEN + BOLD))

            # ASCII Tensor Radar
            lines.append(self._c("│", DIM))
            radar = entry.tensor.render_ascii_radar()
            for rline in radar.splitlines():
                lines.append(self._c("│  ", DIM) + self._c(rline, CYAN))

        lines.append(self._c("└" + "─" * 74 + "┘", RED + BOLD))
        return "\n".join(lines)

    def render_audit_report(self, report: Any, source_lines: Optional[List[str]] = None) -> str:
        """Renders the full supervisor audit report."""
        output = []
        if report.is_sound:
            output.append(self._c("==========================================================================", GREEN + BOLD))
            output.append(self._c("  [✔] 验证闭环达成: 代码符合全部第一性原理与契约不变式 (Zero Defect Energy)", GREEN + BOLD))
            output.append(self._c(f"  状态: {report.status.value} | 耗时: {report.elapsed_ms:.2f}ms | 迭代次数: {report.iteration_count}", CYAN))
            output.append(self._c("==========================================================================", GREEN + BOLD))
            return "\n".join(output)

        output.append(self._c("==========================================================================", RED + BOLD))
        output.append(self._c("  [✘] 拦截严重软件病理缺陷 (Problemology Invariant Violation Detected)", RED + BOLD))
        output.append(self._c(f"  状态: {report.status.value} | 拦截项: {len(report.ast_findings)} 项 | 耗时: {report.elapsed_ms:.2f}ms", YELLOW))
        output.append(self._c("==========================================================================", RED + BOLD))
        output.append("")

        for finding in report.ast_findings:
            output.append(self.render_finding(finding, source_lines=source_lines))
            output.append("")

        if report.tensor_divergence:
            d = report.tensor_divergence
            output.append(self._c("── [ 全域问题散度张量分析 (Problem Divergence Tensor) ] ──────────────", MAGENTA + BOLD))
            output.append(f"  总缺陷势能 (Magnitude): {d.magnitude:.4f}")
            output.append(f"  主导失配流形 (Primary Divergence): {d.primary_divergence.value}")
            output.append(f"  • Δ_IS (意图-规范失配 / 投机作弊) : {d.delta_is:.4f}")
            output.append(f"  • Δ_SE (规范-实现偏差 / 语义故障) : {d.delta_se:.4f}")
            output.append(f"  • Δ_EC (实现-环境失调 / 捷径学习) : {d.delta_ec:.4f}")
            output.append(f"  • Δ_VI (验证神谕假象 / 补丁过拟合) : {d.delta_vi:.4f}")
            output.append(f"  • Δ_T  (系统时空演化 / 认知衰退) : {d.delta_t:.4f}")
            output.append("")

        return "\n".join(output)
