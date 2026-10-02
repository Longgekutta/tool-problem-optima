#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from core.tensor_model import (
    ProblemTensor,
    OntologicalAxis,
    AgencyAxis,
    AbstractionLayerAxis,
    ObservabilityAxis,
    RemediationAxis
)
from core.pathology_catalog import get_catalog_entry, list_all_entries


class TestTensorModel(unittest.TestCase):
    def test_catalog_integrity(self):
        entries = list_all_entries()
        self.assertGreaterEqual(len(entries), 10)
        for e in entries:
            self.assertTrue(e.code.startswith("PRB-"))
            self.assertIsNotNone(e.tensor)
            self.assertEqual(len(e.tensor.vector), 5)
            self.assertIn("■", e.tensor.render_ascii_radar())

    def test_distance_metrics(self):
        e101 = get_catalog_entry("PRB-E101")
        e102 = get_catalog_entry("PRB-E102")
        self.assertIsNotNone(e101)
        self.assertIsNotNone(e102)
        dist = e101.tensor.distance_to(e102.tensor)
        self.assertGreaterEqual(dist, 0.0)
        self.assertLess(dist, 2.0)


if __name__ == "__main__":
    unittest.main()
