"""
Module providing definition of the Color class, implementing Perception's and
the Stimulus' interfaces.
"""

class Color(object):
	"""
	Color represented in CIE L*a*b* space
	"""
	
	def __init__(self,  L, a, b):
		"""
		Initialize Color
		
		http://en.wikipedia.org/wiki/Lab_color_space
		section: Range_of_L.2Aa.2Ab.2A_coordinates
		
		@param L: lightness - should be in [0,100]
		@param a: can be negative
		@param b: can be negative
		"""
		self.L = L
		self.a = a
		self.b = b
	
	
	def to_ML_data(self):
		return [self.L, self.a, self.b]
