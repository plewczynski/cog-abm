import sys
sys.path.append('../')
import unittest

from cog_abm.extras.fitness import *

class TestFitness(unittest.TestCase):

    def test_buffered_average(self):
        ba = get_buffered_average(10)
        self.assertEqual(0, ba.get_fitness())

        for _ in xrange(10):
            ba.add_payoff(5)
            self.assertEqual(5, ba.get_fitness())

        for _ in xrange(10):
            ba.add_payoff(1)
            self.assertTrue(5> ba.get_fitness())

        self.assertEqual(1, ba.get_fitness())

    def test_filling_coverage(self):
        fm = FitnessMeasure()
        self.assertRaises(NotImplementedError, fm.add_payoff, None, None)
        self.assertRaises(NotImplementedError, fm.update_removed, None, None)
        self.assertRaises(NotImplementedError, fm.get_fitness)
