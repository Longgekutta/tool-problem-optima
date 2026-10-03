#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transcript Ingestor: Multi-Editor Zero-Scan Conversation Transcript Discovery
=============================================================================
Elegant, non-brute-force discovery and parsing of AI dialogue transcripts across:
  - Antigravity IDE (~/.gemini/antigravity-ide/brain/<conv_id>/.../transcript.jsonl)
  - Cursor (%APPDATA%/Cursor/User/workspaceStorage/<hash>/state.vscdb & ~/.cursor)
  - VS Code + Cline / Roo-Code (%APPDATA%/Code/User/globalStorage/.../tasks)
  - Windsurf (%APPDATA%/Codeium/Windsurf/User/workspaceStorage)
  - Aider (.aider.chat.history.md in workspace)

Adheres strictly to OS User Data Specifications (XDG / AppData) for sub-5ms discovery.
"""

import os
import sys
import json
import sqlite3
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


@dataclass
class TranscriptEvent:
    """Standardized normalized event in an AI conversation trajectory."""
    index: int
    role: str                          # "user", "assistant", "tool", "system"
    content: str
    thought: str = ""                  # Extracted Chain-of-Thought (<thought> / thinking)
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    tool_results: List[Dict[str, Any]] = field(default_factory=list)
    timestamp: Optional[str] = None
    raw_event: Dict[str, Any] = field(default_factory=dict)


class TranscriptIngestor:
    """Discovers and parses AI transcripts without brute-force filesystem scanning."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()

    def discover_active_transcript(self) -> Optional[Path]:
        """
        Instantly identifies the active AI transcript path using known OS application data locations.
        Priority:
          1. Antigravity IDE active conversation log
          2. Workspace-local Aider log (.aider.chat.history.md)
          3. Cursor workspace-specific / global transcript
          4. VS Code Cline/Roo-Code task transcript
          5. Windsurf workspace transcript
        """
        home = Path.home()
        appdata = Path(os.environ.get("APPDATA", home / "AppData" / "Roaming"))

        # 1. Check Antigravity IDE (Gemini / DeepMind Architecture)
        antigravity_brain = home / ".gemini" / "antigravity-ide" / "brain"
        if antigravity_brain.exists():
            # Find the most recently modified conversation folder with a valid transcript.jsonl
            candidates = list(antigravity_brain.glob("*/.system_generated/logs/transcript.jsonl"))
            if candidates:
                candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                return candidates[0]

        # 2. Check Workspace-local Aider
        aider_log = self.workspace_root / ".aider.chat.history.md"
        if aider_log.exists():
            return aider_log

        # 3. Check Cursor Transcripts
        # Check ~/.cursor/projects/*/agent-transcripts/*.jsonl
        cursor_transcripts = home / ".cursor" / "projects"
        if cursor_transcripts.exists():
            jsonl_candidates = list(cursor_transcripts.glob("*/agent-transcripts/*.jsonl"))
            if jsonl_candidates:
                jsonl_candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                return jsonl_candidates[0]

        # Check Cursor SQLite state.vscdb
        cursor_ws = appdata / "Cursor" / "User" / "workspaceStorage"
        if cursor_ws.exists():
            ws_dbs = list(cursor_ws.glob("*/state.vscdb"))
            if ws_dbs:
                ws_dbs.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                return ws_dbs[0]

        # 4. Check VS Code Cline / Roo-Code
        cline_tasks = appdata / "Code" / "User" / "globalStorage" / "rooveterinaryinc.roo-cline" / "tasks"
        if cline_tasks.exists():
            task_files = list(cline_tasks.glob("*/api_conversation_history.json"))
            if task_files:
                task_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                return task_files[0]

        # 5. Check Windsurf
        windsurf_ws = appdata / "Codeium" / "Windsurf" / "User" / "workspaceStorage"
        if windsurf_ws.exists():
            ws_dbs = list(windsurf_ws.glob("*/state.vscdb"))
            if ws_dbs:
                ws_dbs.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                return ws_dbs[0]

        return None

    def parse_transcript(self, transcript_path: Path) -> List[TranscriptEvent]:
        """Parses any supported transcript file format into normalized TranscriptEvents."""
        if not transcript_path.exists():
            return []

        suffix = transcript_path.suffix.lower()
        if suffix == ".jsonl":
            return self._parse_jsonl(transcript_path)
        elif suffix == ".json":
            return self._parse_json(transcript_path)
        elif suffix in (".vscdb", ".db"):
            return self._parse_sqlite(transcript_path)
        elif suffix == ".md":
            return self._parse_markdown(transcript_path)
        return []

    def _parse_jsonl(self, path: Path) -> List[TranscriptEvent]:
        """Parses standard Antigravity / Cursor JSONL transcripts."""
        events: List[TranscriptEvent] = []
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line_idx, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except Exception:
                    continue

                role = data.get("source", data.get("role", "unknown")).lower()
                step_type = data.get("type", "")
                content = data.get("content", "")
                thought = ""
                tool_calls: List[Dict[str, Any]] = []

                # Extract tool calls
                if "tool_calls" in data and isinstance(data["tool_calls"], list):
                    tool_calls = data["tool_calls"]

                # Extract thinking tags if embedded in content
                if isinstance(content, str):
                    if "<thought>" in content and "</thought>" in content:
                        parts = content.split("<thought>", 1)[1].split("</thought>", 1)
                        thought = parts[0].strip()
                    elif "<thinking>" in content and "</thinking>" in content:
                        parts = content.split("<thinking>", 1)[1].split("</thinking>", 1)
                        thought = parts[0].strip()

                if "thinking" in data:
                    thought = str(data["thinking"])

                # Determine effective role
                norm_role = "assistant" if role in ("model", "assistant", "planner") else ("user" if role in ("user", "user_explicit") else "tool")
                if step_type == "USER_INPUT":
                    norm_role = "user"
                elif step_type in ("PLANNER_RESPONSE", "MODEL"):
                    norm_role = "assistant"

                events.append(TranscriptEvent(
                    index=data.get("step_index", line_idx),
                    role=norm_role,
                    content=content if isinstance(content, str) else json.dumps(content, ensure_ascii=False),
                    thought=thought,
                    tool_calls=tool_calls,
                    timestamp=data.get("timestamp"),
                    raw_event=data
                ))
        return events

    def _parse_json(self, path: Path) -> List[TranscriptEvent]:
        """Parses VS Code Cline / Roo-Code JSON transcripts."""
        events: List[TranscriptEvent] = []
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                data = json.load(f)
            items = data if isinstance(data, list) else data.get("messages", [])
            for idx, item in enumerate(items):
                role = item.get("role", "unknown")
                content = item.get("content", "")
                events.append(TranscriptEvent(
                    index=idx,
                    role=role,
                    content=content if isinstance(content, str) else json.dumps(content, ensure_ascii=False),
                    thought=item.get("thought", ""),
                    tool_calls=item.get("tool_calls", []),
                    raw_event=item
                ))
        except Exception:
            pass
        return events

    def _parse_sqlite(self, path: Path) -> List[TranscriptEvent]:
        """Extracts chat objects from Cursor / Windsurf state.vscdb safely."""
        events: List[TranscriptEvent] = []
        try:
            conn = sqlite3.connect(f"file:{path.as_posix()}?mode=ro", uri=True)
            cursor = conn.cursor()
            # Scan ItemTable or cursorDiskKV
            query = "SELECT key, value FROM ItemTable WHERE key LIKE '%chat%' OR key LIKE '%composer%' LIMIT 100"
            for key, val in cursor.execute(query):
                try:
                    payload = json.loads(val)
                    if isinstance(payload, dict) and "text" in payload:
                        events.append(TranscriptEvent(
                            index=len(events),
                            role=payload.get("sender", "assistant"),
                            content=payload.get("text", ""),
                            raw_event={"key": key}
                        ))
                except Exception:
                    continue
            conn.close()
        except Exception:
            pass
        return events

    def _parse_markdown(self, path: Path) -> List[TranscriptEvent]:
        """Parses Aider Markdown history logs."""
        events: List[TranscriptEvent] = []
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
            blocks = text.split("\n#### ")
            for idx, block in enumerate(blocks):
                if not block.strip():
                    continue
                role = "user" if "User" in block[:20] else "assistant"
                events.append(TranscriptEvent(
                    index=idx,
                    role=role,
                    content=block.strip(),
                    raw_event={"block_header": block[:30]}
                ))
        except Exception:
            pass
        return events
