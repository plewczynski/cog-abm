"""
Module providing environment and it's functionality
"""

import random


class Environment(object):
	"""
	Basic class for stimuli.
	It's main function is to provide stimuli for agents
	"""
	
	def __init__(self,  stimuli):
		"""
		Initialize environment
		
		@param stimuli: initial set of stimuli
		@type stimuli: sequence
		"""
		self.stimuli = stimuli
		

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
		
