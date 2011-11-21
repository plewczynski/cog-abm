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
	
	
	def __init__(self,  stimuli, use_distance = False, distance = 50.):
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
		"""
		Be careful with this - can take some time when using the distance!
		"""
		if not self.use_distance:
			return [self.get_random_stimulus() for _ in xrange(n)]
		
		for _ in xrange(250):
			ret = [self.get_random_stimulus()]
			for _ in xrange(n-1):
				mind = 0
				try_limit = 10
				while mind < self.dist and try_limit>0:
					tmp = self.get_random_stimulus()
					mind = min(imap(tmp.distance, ret))
					try_limit -= 1
				if mind < self.dist:
					break
				ret.append(tmp)
			if len(ret) == n:
				return ret
		raise Exception("Couldn't get samples separated by such distance!")
		
