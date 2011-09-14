import sys
sys.path.append('../')
import unittest
import random
from cog_abm.stimuli.perception import *
from cog_abm.extras.color import Color

class TestColor(unittest.TestCase):
	
		
	def test_init_perceptionColor(self):
		"""
		Test of giving random content to the color instance.
		"""
		
		random.seed()
		L = random.random()
		a = random.randint(0, 255)
		b = random.randint(0, 255)
		col = Color(L, a, b)
		per_col = SimplePerception(col)
		self.assertEqual(per_col.content, col)
		self.assertEqual(per_col.content.to_ML_data(), [L, a, b])
		self.assertEqual(isinstance(per_col, SimplePerception), True)
		self.assertEqual(isinstance(per_col, Perception), True)
	
if __name__ == '__main__':
    unittest.main()
