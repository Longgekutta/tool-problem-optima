#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from engine.metamorphic_oracle import MetamorphicOracleEngine


class TestMetamorphicOracle(unittest.TestCase):
    def setUp(self):
        self.oracle = MetamorphicOracleEngine(seed=123)

    def test_idempotence_pass(self):
        # abs(abs(x)) == abs(x)
        res = self.oracle.test_idempotence(abs, [-5, 10, -100, 0])
        self.assertIsNone(res)

    def test_idempotence_violation(self):
        # Non-idempotent increment: f(f(x)) != f(x)
        res = self.oracle.test_idempotence(lambda x: x + 1, [1, 2, 3])
        self.assertIsNotNone(res)
        self.assertEqual(res.relation_name, "MR-IDEMPOTENCE")

    def test_commutativity_pass(self):
        # a + b == b + a
        res = self.oracle.test_commutativity(lambda a, b: a + b, [(1, 2), (10, 20)])
        self.assertIsNone(res)

    def test_commutativity_violation(self):
        # Asymmetric function: a - b != b - a
        res = self.oracle.test_commutativity(lambda a, b: a - b, [(5, 2), (10, 1)])
        self.assertIsNotNone(res)
        self.assertEqual(res.relation_name, "MR-COMMUTATIVITY")

    def test_adversarial_overfitting_caught(self):
        # Overfitted function that only returns 100 for (42, "bug"), returns garbage for others
        def overfitted_patch(x, y):
            if x == 42 and y == "bug":
                return 100
            return 0  # wrong default

        known_inputs = [(42, "bug")]
        # Perturbation: shift 42 to 43 or "bug" to "bug_sub"
        violations = self.oracle.test_adversarial_overfitting(
            candidate_fn=overfitted_patch,
            known_test_inputs=known_inputs,
            perturbation_generator=lambda val: val + 1 if isinstance(val, int) else val,
            ground_truth_validator=lambda args, out: out == 101 if args[0] == 43 else True
        )
        self.assertGreater(len(violations), 0)
        self.assertEqual(violations[0].relation_name, "MR-ANTI-OVERFITTING")


if __name__ == "__main__":
    unittest.main()
