#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for TranscriptIngestor and ContextDistillerBridge.
"""

import unittest
import tempfile
import json
from pathlib import Path

from engine.transcript_ingestor import TranscriptIngestor, TranscriptEvent
from engine.context_distiller_bridge import ContextDistillerBridge, TriAnchorSlice


class TestTranscriptIngestor(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.dir_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_jsonl_parsing(self):
        jsonl_file = self.dir_path / "sample_transcript.jsonl"
        lines = [
            json.dumps({"type": "USER_INPUT", "content": "Fix the sorting algorithm", "step_index": 0}),
            json.dumps({
                "type": "PLANNER_RESPONSE",
                "content": "<thought>I will fix the boundary condition in sort function</thought>I am fixing it now.",
                "tool_calls": [{"name": "run_command", "args": {"CommandLine": "python sort.py"}}],
                "step_index": 1
            })
        ]
        jsonl_file.write_text("\n".join(lines), encoding="utf-8")

        ingestor = TranscriptIngestor(workspace_root=self.dir_path)
        events = ingestor.parse_transcript(jsonl_file)

        self.assertEqual(len(events), 2)
        self.assertEqual(events[0].role, "user")
        self.assertIn("Fix the sorting", events[0].content)
        self.assertEqual(events[1].role, "assistant")
        self.assertIn("boundary condition", events[1].thought)
        self.assertEqual(len(events[1].tool_calls), 1)

    def test_distiller_tri_anchor_extraction(self):
        # Multi-turn history with noisy tool outputs and system context
        events = [
            TranscriptEvent(
                index=0,
                role="system",
                content="System Instructions: You are an expert AI software engineer. " * 50
            ),
            TranscriptEvent(
                index=1,
                role="user",
                content="<USER_REQUEST>Implement robust binary search</USER_REQUEST>"
            ),
            TranscriptEvent(
                index=2,
                role="assistant",
                content="<thought>Checking midpoint calculation to avoid integer overflow</thought>Done.",
                thought="Checking midpoint calculation to avoid integer overflow",
                tool_calls=[{"name": "write_to_file", "args": {"TargetFile": "D:/github/project/search.py"}}]
            ),
            TranscriptEvent(
                index=3,
                role="tool",
                content="Created file search.py successfully. " * 30
            )
        ]

        bridge = ContextDistillerBridge(workspace_root=self.dir_path)
        causal_slice = bridge.distill_tri_anchor_slice(events)

        self.assertEqual(causal_slice.user_intent, "Implement robust binary search")
        self.assertIn("integer overflow", causal_slice.reasoning_claims)
        self.assertEqual(len(causal_slice.action_calls), 1)
        self.assertIn("search.py", causal_slice.mutated_files[0])
        self.assertGreater(causal_slice.compression_ratio, 50.0)


if __name__ == "__main__":
    unittest.main()
