#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from core.pathology_catalog import (
    list_all_entries,
    list_categories,
    list_by_category,
    get_catalog_entry
)


class TestCatalogExpansion(unittest.TestCase):
    def test_full_catalog_volume(self):
        entries = list_all_entries()
        self.assertGreaterEqual(len(entries), 30)

    def test_six_categories_presence(self):
        cats = list_categories()
        self.assertEqual(len(cats), 6)
        expected = [
            "Agentic Tooling & Environment",
            "Algorithmic Synthesis & Logic",
            "Architecture & Concurrency",
            "Context & Cognitive",
            "Security & Supply Chain",
            "Testing, Oracle & Epistemic"
        ]
        for exp in expected:
            self.assertIn(exp, cats)
            items = list_by_category(exp)
            self.assertGreater(len(items), 0)

    def test_sample_pathologies(self):
        # PRB-E503: Secret leak
        e503 = get_catalog_entry("PRB-E503")
        self.assertIsNotNone(e503)
        self.assertEqual(e503.category, "Security & Supply Chain")

        # PRB-E001: Context satiation
        e001 = get_catalog_entry("PRB-E001")
        self.assertIsNotNone(e001)
        self.assertEqual(e001.category, "Context & Cognitive")

        # PRB-E301: TOCTOU
        e301 = get_catalog_entry("PRB-E301")
        self.assertIsNotNone(e301)
        self.assertEqual(e301.category, "Architecture & Concurrency")


if __name__ == "__main__":
    unittest.main()
