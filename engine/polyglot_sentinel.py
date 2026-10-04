#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Polyglot Sentinel: Multi-Language Lexical & Pattern Invariant Verifier
=====================================================================
Extends the verification horizon of tool-problem-optima beyond Python to:
  - JavaScript / TypeScript (.js, .jsx, .ts, .tsx)
  - C / C++ (.c, .cc, .cpp, .h, .hpp)
  - Go (.go)

Detects universal software pathologies across languages:
  - PRB-E104: Trivial / Tautological Assertions in tests
  - PRB-E108: Silent Exception Swallow (Empty catch blocks / blank error discard)
  - PRB-E203: Floating Point Precision Loss (Direct equality with float literals)
  - PRB-E204: Banned Vulnerable Functions (e.g. gets in C)
  - PRB-E301: TOCTOU Race Condition (access() then fopen() in C/C++)
  - PRB-E303: Unbounded Resource Descriptor Leak (open without close)
  - PRB-E304: Cascading Concurrency Explosion (Unbounded 'go func()' in loops)
  - PRB-E502: Dependency Bloat (Wildcard 'import * as ...')
  - PRB-E503: Hardcoded Secret / Credential Leak

Zero external dependencies. Sub-5ms evaluation per file.
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Optional, Any, Set
from pathlib import Path


@dataclass
class PolyglotFinding:
    """A diagnostic violation identified in non-Python source code."""
    code: str
    name: str
    language: str
    file_path: str
    line_number: int
    snippet: str
    message: str
    remediation_suggestion: str


def _strip_comments_preserving_lines(text: str) -> str:
    """Strips // line comments and /* */ block comments while preserving line count."""
    def replacer(match):
        s = match.group(0)
        if s.startswith("/"):
            return "\n" * s.count("\n")
        return s

    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)


class PolyglotSentinel:
    """Multi-language static pattern and structural verifier."""

    SUPPORTED_EXTENSIONS = {
        ".js": "javascript",
        ".jsx": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".c": "c",
        ".cc": "cpp",
        ".cpp": "cpp",
        ".h": "c_header",
        ".hpp": "cpp_header",
        ".go": "go"
    }

    def audit_source(self, source_code: str, file_path: str = "<source>") -> List[PolyglotFinding]:
        """Audits source code based on its file extension."""
        ext = Path(file_path).suffix.lower()
        lang = self.SUPPORTED_EXTENSIONS.get(ext)
        if not lang:
            return []

        findings: List[PolyglotFinding] = []
        lines = source_code.splitlines()

        # Universal Check: PRB-E503 Hardcoded Secrets
        secret_pattern = re.compile(r"""(?:ghp_|sk-|AKIA)[a-zA-Z0-9_\-]{16,}""")
        for idx, line in enumerate(lines, 1):
            if secret_pattern.search(line):
                findings.append(PolyglotFinding(
                    code="PRB-E503",
                    name="Hardcoded Secret / Credential Leak",
                    language=lang,
                    file_path=file_path,
                    line_number=idx,
                    snippet=line.strip(),
                    message="Detected plaintext private API token/credential in source.",
                    remediation_suggestion="Isolate secrets in environment variables or vault; do not hardcode in source."
                ))

        # Language-Specific Audits
        if lang in ("javascript", "typescript"):
            findings.extend(self._audit_javascript(source_code, lines, file_path, lang))
        elif lang in ("c", "cpp", "c_header", "cpp_header"):
            findings.extend(self._audit_c_cpp(source_code, lines, file_path, lang))
        elif lang == "go":
            findings.extend(self._audit_go(source_code, lines, file_path, lang))

        return findings

    def _audit_javascript(self, content: str, lines: List[str], file_path: str, lang: str) -> List[PolyglotFinding]:
        findings = []
        clean_content = _strip_comments_preserving_lines(content)

        # PRB-E108: Empty catch block: catch (...) { } across single or multiple lines
        for m in re.finditer(r"""catch\s*\([^)]*\)\s*\{\s*\}""", clean_content, flags=re.DOTALL):
            lineno = clean_content[:m.start()].count("\n") + 1
            snippet = lines[lineno - 1].strip() if 0 <= lineno - 1 < len(lines) else m.group(0).replace("\n", " ").strip()
            findings.append(PolyglotFinding(
                code="PRB-E108",
                name="Silent Exception Swallow (Empty Catch Block)",
                language=lang,
                file_path=file_path,
                line_number=lineno,
                snippet=snippet,
                message="Empty catch block silently swallows runtime errors without logging or handling.",
                remediation_suggestion="Log the caught error or re-throw appropriately: catch (err) { console.error(err); throw err; }."
            ))

        for idx, line in enumerate(lines, 1):
            # Skip pure comment lines
            stripped = line.strip()
            if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
                continue

            # PRB-E203: Exact float equality: === 0.1 or == 0.1
            if re.search(r"""={2,3}\s*0\.\d+""", line) or re.search(r"""0\.\d+\s*={2,3}""", line):
                findings.append(PolyglotFinding(
                    code="PRB-E203",
                    name="Floating Point Non-Associativity (Exact Float Equality)",
                    language=lang,
                    file_path=file_path,
                    line_number=idx,
                    snippet=stripped,
                    message="Direct equality comparison with fractional float literal risks precision loss.",
                    remediation_suggestion="Use Math.abs(a - b) < Number.EPSILON for floating point comparisons."
                ))

            # PRB-E502: Wildcard import: import * as foo from '...'
            if re.search(r"""import\s+\*\s+as\s+\w+\s+from""", line):
                findings.append(PolyglotFinding(
                    code="PRB-E502",
                    name="Dependency Bloat & Namespace Pollution (Wildcard Import)",
                    language=lang,
                    file_path=file_path,
                    line_number=idx,
                    snippet=stripped,
                    message="Wildcard 'import * as ...' pulls entire module into bundle, hindering tree-shaking.",
                    remediation_suggestion="Import only explicit required named exports: import { specificFn } from '...'."
                ))

            # PRB-E104: Trivial test assertion
            if re.search(r"""expect\s*\(\s*true\s*\)\s*\.\s*(?:toBe|toEqual)\s*\(\s*true\s*\)""", line) or re.search(r"""assert\s*\(\s*(?:true|1\s*==\s*1)\s*\)""", line):
                findings.append(PolyglotFinding(
                    code="PRB-E104",
                    name="Tautological Verification (Trivial Test Assertion in JS/TS)",
                    language=lang,
                    file_path=file_path,
                    line_number=idx,
                    snippet=stripped,
                    message="Tautological assertion provides zero verification power.",
                    remediation_suggestion="Assert meaningful invariant properties or actual returned state."
                ))

        # PRB-E303: Unclosed fs.openSync
        if re.search(r"""\bfs\.openSync\s*\(""", clean_content) and not re.search(r"""\bfs\.closeSync\s*\(""", clean_content):
            findings.append(PolyglotFinding(
                code="PRB-E303",
                name="Unbounded Resource Descriptor Leak (fs.openSync without closeSync)",
                language=lang,
                file_path=file_path,
                line_number=1,
                snippet="fs.openSync(...) without matching fs.closeSync(...)",
                message="Opening file descriptor via fs.openSync without corresponding fs.closeSync leaks file handles.",
                remediation_suggestion="Always close file descriptors in a finally block with fs.closeSync(fd)."
            ))

        return findings

    def _audit_c_cpp(self, content: str, lines: List[str], file_path: str, lang: str) -> List[PolyglotFinding]:
        findings = []
        clean_content = _strip_comments_preserving_lines(content)

        # PRB-E108: Empty catch block: catch (...) { } across single or multiple lines
        for m in re.finditer(r"""catch\s*\([^)]*\)\s*\{\s*\}""", clean_content, flags=re.DOTALL):
            lineno = clean_content[:m.start()].count("\n") + 1
            snippet = lines[lineno - 1].strip() if 0 <= lineno - 1 < len(lines) else m.group(0).replace("\n", " ").strip()
            findings.append(PolyglotFinding(
                code="PRB-E108",
                name="Silent Exception Swallow (Empty Catch-All Block)",
                language=lang,
                file_path=file_path,
                line_number=lineno,
                snippet=snippet,
                message="Empty 'catch (...)' block suppresses all C++ exceptions without diagnosis.",
                remediation_suggestion="Catch specific std::exception and log e.what() before graceful termination."
            ))

        # PRB-E301: TOCTOU: access() followed by fopen()
        if re.search(r"""\baccess\s*\([^)]*\)""", clean_content) and re.search(r"""\bfopen\s*\([^)]*\)""", clean_content):
            findings.append(PolyglotFinding(
                code="PRB-E301",
                name="Time-of-Check to Time-of-Use Race Condition (TOCTOU in C/C++)",
                language=lang,
                file_path=file_path,
                line_number=1,
                snippet="access(...) followed by fopen(...)",
                message="Checking file permissions with access() before fopen() introduces a TOCTOU symlink/race condition.",
                remediation_suggestion="Open file directly with fopen() and inspect errno / handle NULL return value."
            ))

        # PRB-E204: Banned dangerous functions
        for idx, line in enumerate(lines, 1):
            if re.search(r"""\bgets\s*\(""", line):
                findings.append(PolyglotFinding(
                    code="PRB-E204",
                    name="Banned Vulnerable Function (CWE-242 gets)",
                    language=lang,
                    file_path=file_path,
                    line_number=idx,
                    snippet=line.strip(),
                    message="Use of inherently unsafe gets() function causes buffer overflow vulnerabilities.",
                    remediation_suggestion="Replace gets() with fgets() specifying exact buffer capacity."
                ))

        # PRB-E303: fopen without fclose
        if re.search(r"""\bfopen\s*\(""", clean_content) and not re.search(r"""\bfclose\s*\(""", clean_content):
            findings.append(PolyglotFinding(
                code="PRB-E303",
                name="Unbounded Resource Descriptor Leak (fopen without fclose)",
                language=lang,
                file_path=file_path,
                line_number=1,
                snippet="fopen(...) without matching fclose(...)",
                message="Opening file pointer via fopen without corresponding fclose leaks file descriptors.",
                remediation_suggestion="Ensure fclose() is called on all code paths or use RAII wrappers (std::unique_ptr with custom deleter)."
            ))

        return findings

    def _audit_go(self, content: str, lines: List[str], file_path: str, lang: str) -> List[PolyglotFinding]:
        findings = []
        clean_content = _strip_comments_preserving_lines(content)

        # PRB-E108: Blank error swallow: _ = err or _, _ = err
        for idx, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("//"):
                continue
            if re.search(r"""\b_\s*=\s*err\b""", line) or re.search(r"""\b_\s*,\s*_\s*=\s*err\b""", line):
                findings.append(PolyglotFinding(
                    code="PRB-E108",
                    name="Silent Exception Swallow (Blank Identifier Error Discard in Go)",
                    language=lang,
                    file_path=file_path,
                    line_number=idx,
                    snippet=stripped,
                    message="Assigning error to blank identifier '_ = err' explicitly ignores critical failures.",
                    remediation_suggestion="Check error explicitly: 'if err != nil { return err }'."
                ))

        # PRB-E304: go func() in loop
        in_loop = False
        loop_brace_depth = 0
        for idx, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("//"):
                continue
            if re.search(r"""\bfor\b""", line):
                in_loop = True
                loop_brace_depth += line.count("{") - line.count("}")
            elif in_loop:
                loop_brace_depth += line.count("{") - line.count("}")
                if re.search(r"""\bgo\s+(?:func\(|[a-zA-Z_]\w*\()""", line):
                    findings.append(PolyglotFinding(
                        code="PRB-E304",
                        name="Cascading Concurrency Explosion (Unbounded Goroutine in Loop)",
                        language=lang,
                        file_path=file_path,
                        line_number=idx,
                        snippet=stripped,
                        message="Spawning goroutines directly inside a loop without a worker pool or semaphore can exhaust OS threads.",
                        remediation_suggestion="Use a bounded worker pool (e.g. channel semaphore or sync.WaitGroup with worker count)."
                    ))
                if loop_brace_depth <= 0:
                    in_loop = False

        # PRB-E303: os.Open without Close
        if re.search(r"""\bos\.Open\s*\(""", clean_content) and not re.search(r"""\.Close\s*\(\)""", clean_content):
            findings.append(PolyglotFinding(
                code="PRB-E303",
                name="Unbounded Resource Descriptor Leak (os.Open without Close in Go)",
                language=lang,
                file_path=file_path,
                line_number=1,
                snippet="os.Open(...) without .Close()",
                message="Opening file via os.Open without defer f.Close() leaks file handles.",
                remediation_suggestion="Ensure 'defer file.Close()' immediately follows successful os.Open call."
            ))

        return findings
