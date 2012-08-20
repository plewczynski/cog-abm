import os
import random
import unittest

from itertools import chain, izip

from cog_abm.extras.numeric_results_collection import NumericResultCollector


class TestNumericResulCollector(unittest.TestCase):

    def setUp(self):
        self.N = 10
        self.columns = [
            range(self.N),
            [random.randint(0, 2 * self.N) for _ in xrange(self.N)],
            [random.random() for _ in xrange(self.N)],
            ]

    def test_add_and_save(self):
        rc = NumericResultCollector()
        rc.add_column(self.columns[0], 'x')
        rc.add_column(self.columns[1])
        rc.add_column(self.columns[2], 'error rate')
        # FIXME: I know this is ugly ..
        fname = 'test_file_for_numeric_result_collector'
        rc.save(fname)
        rcn = NumericResultCollector.load(fname)
        self.assertEqual(rc.column_names, rcn.column_names)
        [self.assertAlmostEqual(x, y, 8) for x, y in
                izip(chain(*rc.columns), chain(*rcn.columns))]
        os.remove(fname)
