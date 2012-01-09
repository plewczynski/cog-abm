"""
Module providing environment and it's functionality
"""

import random
from itertools import imap


class StimuliChooser(object):
	
	def __init__(self, n=None):
		self.n = n
	
	def get_stimulus(self, stimuli):
		return random.choice(stimuli)
	
	def get_stimuli(self, stimuli, n=None):
		pass


class RandomStimuliChooser(StimuliChooser):
	
	def __init__(self, n=None, use_distance=False, distance=50.):
		super(RandomStimuliChooser, self).__init__(n)
		self.use_distance = use_distance
		self.distance = distance
	
	def get_stimuli(self, stimuli, n=None):
		"""
		Be careful with this - can take some time when using the distance!
		"""
		n = n or self.n
		if not self.use_distance:
			return [self.get_stimulus(stimuli) for _ in xrange(n)]
		
		for _ in xrange(250):
			ret = [self.get_stimulus(stimuli)]
			for _ in xrange(n-1):
				mind = 0
				try_limit = 10
				while mind < self.distance and try_limit>0:
					tmp = self.get_stimulus(stimuli)
					mind = min(imap(tmp.distance, ret))
					try_limit -= 1
				if mind < self.distance:
					break
				ret.append(tmp)
			if len(ret) == n:
				return ret
		raise Exception("Couldn't get samples separated by such distance!")
		

class OneDifferentClass(StimuliChooser):
	"""
	This will return first sample of class different than others.
	This is important if we have binary classification and contex of size 4
	"""
	
	def __init__(self, n=None):
		self.n = n
	
	def get_stimuli(self, stimuli, n=None):
		n = n or self.n
		for _ in xrange(100):
			ret = [self.get_stimulus(stimuli)]
			cls = ret[0].get_cls()
			for _ in xrange(n-1):
				try_limit = 100
				while try_limit>0:
					tmp = self.get_stimulus(stimuli)
					if cls != tmp.get_cls():
						break
					try_limit -= 1
				if cls == tmp.get_cls():
					break
				ret.append(tmp)
			if len(ret) == n:
				return ret
		raise Exception("Couldn't get samples in different classes")


class Environment(object):
	"""
	Basic class for stimuli.
	It's main function is to provide stimuli for agents
	"""
	
	
	def __init__(self,  stimuli, stimuli_chooser=None):
		"""
		Initialize environment
		
		@param stimuli: initial set of stimuli
		@type stimuli: sequence
		"""
		self.stimuli = stimuli
		self.stimuli_chooser = stimuli_chooser or RandomStimuliChooser(1)
		
	def get_stimulus(self):
		"""
		Gives stimulus from the set of available stimuli
		
		@return: random stimulus
		@rtype: Stimulus
		"""
		return self.stimuli_chooser.get_stimulus(self.stimuli)
	
	def get_all_stimuli(self):
		"""
		Gives set of all stimuli available in the environment
		
		@return: sequence of stimuli
		@rtype: sequence
		"""
		return self.stimuli

	def get_stimuli(self, n):
		return self.stimuli_chooser.get_stimuli(self.stimuli, n)

