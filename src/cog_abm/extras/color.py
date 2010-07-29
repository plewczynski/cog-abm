"""
Module providing definition of the Color class, implementing Perception's and the Stimulus' interfaces.
"""
import stimulus
import sys
import perception

class Color(stimulus.Stimulus, perception.Perception):
	"""
	Color making for both Stimulus and Perception in basic Steel's experiment. The list of 3 values in CIE 
    space denotes one color: L, a, b.
	"""
	
	def __init__(self,  L=0, a=0, b=0):
		"""
		Initialize Color
		
		@param content: list of objects that constitute the Color
		@type stimuli: sequence
		"""
		self.content = [L, a, b]
	