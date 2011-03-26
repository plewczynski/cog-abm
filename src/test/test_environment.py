import sys
sys.path.append('../')
import unittest
from cog_abm.core.environment import *


class TestEnvironment(unittest.TestCase):
	
	def setUp(self):
		pass
		
	def test_get_random_stimulus(self):
		""" Does environment gives proper random stimuli - form given sequence
		"""
		set = range(10)
		env = Environment(set)
		for i in range(100):
			self.assertTrue(env.get_random_stimulus() in set)
			
	def test_get_all_stimuli(self):
		""" Does environment returns proper sequence of stimuli - given earlier
		"""
		env = Environment(range(10))
		self.assertEqual(env.get_all_stimuli(),  range(10))
			

	

if __name__ == '__main__':
    unittest.main()
