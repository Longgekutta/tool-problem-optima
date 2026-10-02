#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from core.problemology import (
    SpaceCoordinates,
    compute_tensor_divergence,
    DivergenceType
)


class TestProblemology(unittest.TestCase):
    def test_ideal_state_zero_divergence(self):
        ideal = SpaceCoordinates(1.0, 1.0, 1.0, 1.0)
        self.assertTrue(ideal.is_ideal())
        div = compute_tensor_divergence(ideal)
        self.assertAlmostEqual(div.magnitude, 0.0, places=4)

    def test_patch_overfitting_divergence(self):
        # High exec soundness on weak spec, low intent fidelity
        coords = SpaceCoordinates(
            intent_fidelity=0.3,
            spec_coverage=0.4,
            exec_soundness=1.0,
            context_resilience=0.4
        )
        div = compute_tensor_divergence(coords)
        self.assertGreater(div.magnitude, 0.5)
        # Delta_VI should be high because execution passed without intent
        self.assertGreater(div.delta_vi, 0.5)
        self.assertEqual(div.primary_divergence, DivergenceType.EPISTEMIC)

    def test_specification_gaming_divergence(self):
        # Intent is high, but spec is narrow, gaming occurs
        coords = SpaceCoordinates(
            intent_fidelity=1.0,
            spec_coverage=0.2,
            exec_soundness=1.0,
            context_resilience=0.3
        )
        div = compute_tensor_divergence(coords)
        self.assertGreater(div.delta_is, 0.7)


if __name__ == "__main__":
    unittest.main()
