import unittest

import random

import color
import stimulus
import perception


class TestColor(unittest.TestCase):
    """
	Test class for Color class..
	"""
	
	def test_init_color(self):
		"""Test of giving random content to the color instance.
		"""
		
		random.seed()
		L = random.random()
		a = random.randint(0, 255)
		b = random.randint(0, 255)        
		col = color.Color(L, a, b)
		self.assertEqual(col.get_content(), [L, a, b])
	
if __name__ == '__main__':
    unittest.main()
