import sys
sys.path.append('../')
import unittest
import random
from cog_abm.extras.color import Color


class TestColor(unittest.TestCase):
	
	def test_init_color(self):
		"""
		Test of giving random content to the color instance.
		"""
		
		random.seed()
		L = random.random()
		a = random.randint(0, 255)
		b = random.randint(0, 255)        
		col = Color([L, a, b])
		self.assertEqual(col.content, [L, a, b])
	
if __name__ == '__main__':
    unittest.main()
