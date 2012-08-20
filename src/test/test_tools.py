import sys

sys.path.append('../')

import unittest
from cog_abm.extras.tools import calc_auc


class TestAucCalculations(unittest.TestCase):

    def setUp(self):
        pass

    def test_auc(self):
        test_data = [
            ([(0, 0), (1, 2), (2, 0)], 2.),
            ([(0, 1), (1, 1)], 1),
            ([(0., 0.5), (1, 2), (2, 2.)], 1.25 + 2.)
            ]
        for curve, expected_auc in test_data:
            self.assertEqual(expected_auc, calc_auc(curve))
