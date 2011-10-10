"""
Module providing environment and it's functionality
"""

import random
from itertools import imap

class Environment(object):
	"""
	Basic class for stimuli.
	It's main function is to provide stimuli for agents
	"""
	
	
	def __init__(self,  stimuli, use_distance = False, distance = 45.):
		"""
		Initialize environment
		
		@param stimuli: initial set of stimuli
		@type stimuli: sequence
		"""
		self.stimuli = stimuli
		self.use_distance = use_distance
		self.dist = float(distance)
		

	def get_random_stimulus(self):
		"""
		Gives random stimulus from the set of available stimuli
		
		@return: random stimulus
		@rtype: Stimulus
		"""
		return random.choice(self.stimuli)
	
	
	def get_all_stimuli(self):
		"""
		Gives set of all stimuli available in the environment
		
		@return: sequence of stimuli
		@rtype: sequence
		"""
		return self.stimuli
		

	def get_random_stimuli(self, n):
		if not self.use_distance:
			return [self.get_random_stimulus() for _ in xrange(n)]
		
		ret = [self.get_random_stimulus()]
		for _ in xrange(n-1):
			
			mind = 0
			while mind < self.dist:
				tmp = self.get_random_stimulus()
				mind = min(imap(tmp.distance, ret))
			ret.append(tmp)
		
		return ret
		
