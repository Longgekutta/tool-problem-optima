#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import tempfile
import argparse
from pathlib import Path
from main import cmd_preflight


class TestPreflightGate(unittest.TestCase):
    def test_preflight_on_clean_workspace(self):
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td)
            clean_file = ws / "clean_module.py"
            clean_file.write_text(
                "import os\n\ndef add(a: int, b: int) -> int:\n    return a + b\n",
                encoding="utf-8"
            )
            args = argparse.Namespace(workspace=str(ws), target=str(clean_file), json=True)
            res = cmd_preflight(args)
            self.assertEqual(res, 0, "Preflight on clean module must exit with 0")

    def test_preflight_blocks_tautological_and_phantom_code(self):
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td)
            toxic_file = ws / "test_toxic.py"
            toxic_file.write_text(
                "import fast_sort_3d_slop\n\ndef test_fake():\n    assert True\n",
                encoding="utf-8"
            )
            args = argparse.Namespace(workspace=str(ws), target=str(toxic_file), json=True)
            res = cmd_preflight(args)
            self.assertEqual(res, 1, "Preflight on toxic code must block and exit with 1")


if __name__ == "__main__":
    unittest.main()
