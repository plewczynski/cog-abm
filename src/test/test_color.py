import sys
sys.path.append('../')
import unittest
import random
from cog_abm.extras.color import Color
import math


class TestColor(unittest.TestCase):

    def test_init_color(self):
        """
        Test of giving random content to the color instance.
        """

        random.seed()
        for _ in xrange(20):
            L = random.randint(0, 100)
            a = random.randint(-255, 255)
            b = random.randint(-255, 255)
            col = Color(L, a, b)
            self.assertEqual(col.get_values(), [L, a, b])


    def test_distance(self):
        """
        similar color
        """
        for _ in xrange(20):
            L = random.randint(0, 100)
            a = random.randint(-255, 255)
            b = random.randint(-255, 255)
            col = Color(L, a, b)
            self.assertTrue(col.distance(col) == 0.)

        a = Color(5, 3, 3)
        b = Color(6, 1, -1)
        self.assertTrue(math.fabs(a.distance(b) - 4.58257) < 0.00001)



if __name__ == '__main__':
    unittest.main()
