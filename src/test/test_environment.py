import sys
sys.path.append('../')
import unittest
from cog_abm.core.environment import *
from cog_abm.ML.core import Sample


class TestEnvironment(unittest.TestCase):
	
	def setUp(self):
		pass
		
	def test_get_random_stimulus(self):
		""" Does environment gives proper random stimuli - form given sequence
		"""
		stimuli = range(10)
		env = Environment(stimuli)
		for _ in range(100):
			self.assertTrue(env.get_random_stimulus() in stimuli)
			
	def test_get_all_stimuli(self):
		""" Does environment returns proper sequence of stimuli - given earlier
		"""
		env = Environment(range(10))
		self.assertEqual(env.get_all_stimuli(),  range(10))
		
	def test_random_stimuli_with_distance(self):
		samples = [Sample([x]) for x in xrange(10)]*10
		env = Environment(samples, True, 3)
		for _ in xrange(10):
			sort = sorted([x.get_values()[0] for x in env.get_random_stimuli(4)])
			self.assertEqual([0, 3, 6, 9], sort)
			
		env = Environment(samples, True, 5)
		for _ in xrange(10):
			sort = sorted([x.get_values()[0] for x in env.get_random_stimuli(2)])
			self.assertEqual(len(sort), 2)
			self.assertTrue(sort[0] < 5)
			self.assertTrue(sort[1] >= 5)
	

if __name__ == '__main__':
	unittest.main()
	
