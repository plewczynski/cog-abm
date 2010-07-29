"""
Module providing definition of the Color class, implementing Perception's and
the Stimulus' interfaces.
"""

class Color(object):
	"""
	The list of 3 values in CIE: L, a, b in this order. First value should be a
	float value from range [0,1], a and b should be integers from range [0,255].
	"""
	
	def __init__(self,  content):
		"""
		Initialize Color
		
		@param content: list of numbers that constitute the Color
		@type content: sequence
		"""
		self.content = content