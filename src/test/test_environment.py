import unittest
from cog_abm.core.environment import *
from cog_abm.ML.core import Sample, load_samples_arff

class TestChoosers(unittest.TestCase):
	
	def setUp(self):
		self.samples = load_samples_arff("test/iris.arff")
		
	def test_OneDifferent_getting_stimuli(self):
		chooser = OneDifferentClass(4)
		
		for _ in xrange(100):
			samples = chooser.get_stimuli(self.samples)
			clss = [x.get_cls() for x in samples]
			self.assertEqual(1, clss.count(clss[0]))
	
	def test_OneDifferent_unable_to_get(self):
		samples = [x for x in self.samples
				if x.get_cls == self.samples[0].get_cls]
		chooser = OneDifferentClass(40)
		self.assertRaises(Exception, chooser.get_stimuli, samples)


class TestEnvironment(unittest.TestCase):
	
	def setUp(self):
		pass
		
	def test_get_random_stimulus(self):
		""" Does environment gives proper random stimuli - form given sequence
		"""
		stimuli = range(10)
		env = Environment(stimuli)
		for _ in range(100):
			self.assertTrue(env.get_stimulus() in stimuli)
			
	def test_get_all_stimuli(self):
		""" Does environment returns proper sequence of stimuli - given earlier
		"""
		env = Environment(range(10))
		self.assertEqual(env.get_all_stimuli(),  range(10))
		
	def test_random_stimuli_with_distance(self):
		samples = [Sample([x]) for x in xrange(10)]*10
		chooser = RandomStimuliChooser(None, True, 3)
		env = Environment(samples, chooser)
		for _ in xrange(10):
			sort = sorted([x.get_values()[0] for x in env.get_stimuli(4)])
			self.assertEqual([0, 3, 6, 9], sort)
		
		chooser = RandomStimuliChooser(None, True, 5)
		env = Environment(samples, chooser)
		for _ in xrange(10):
			sort = sorted([x.get_values()[0] for x in env.get_stimuli(2)])
			self.assertEqual(len(sort), 2)
			self.assertTrue(sort[0] < 5)
			self.assertTrue(sort[1] >= 5)
		
		self.assertRaises(Exception, chooser.get_stimuli, samples, 100)
	
	def test_random_without_distance(self):
		stimuli = range(10)
		chooser = RandomStimuliChooser(4, False)
		for _ in xrange(50):
			for x in chooser.get_stimuli(stimuli):
				self.assertTrue(x in stimuli)
	

if __name__ == '__main__':
	unittest.main()
	
