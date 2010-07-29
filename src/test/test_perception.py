import sys
sys.path.append('../')
import unittest
import random
from cog_abm.stimuli.perception import *
from cog_abm.extras.color import Color

class TestColor(unittest.TestCase):
	
	def test_init_perception(self):
		"""
		Test of giving random content to the color instance.
		"""
		
		perc = Perception()
		
		
		self.assertEqual(isinstance(perc, Perception), True)
		
	def test_init_perceptionColor(self):
		"""
		Test of giving random content to the color instance.
		"""
		
		random.seed()
		L = random.random()
		a = random.randint(0, 255)
		b = random.randint(0, 255)        
		col = Color([L, a, b])
		per_col = PerceptionColor(col)
		self.assertEqual(per_col.color, col)
		self.assertEqual(per_col.color.content, [L, a, b])
		self.assertEqual(isinstance(per_col, Perception), True)
		self.assertEqual(isinstance(per_col, PerceptionColor), True)
	
if __name__ == '__main__':
    unittest.main()
