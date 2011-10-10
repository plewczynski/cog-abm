"""
Module providing definition of the Color class, implementing Perception's and
the Stimulus' interfaces.
"""
import math
from itertools import izip
from cog_abm.ML.core import Sample, euclidean_distance


class Color(Sample):
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
		super(Color, self).__init__([L, a, b], dist_fun=euclidean_distance)
		self.L = L
		self.a = a
		self.b = b
	
#	
#	def to_ML_data(self):
#		return [self.L, self.a, self.b]

#
#	def distance(self, other):
#		l = izip(self.to_ML_data(), other.to_ML_data())
#		return math.sqrt(math.fsum([(x-y)**2 for x, y in l]))
	
#	
#	def __eq__(self, other):
#		return self.L == other.L and self.a == other.a and self.b == other.b



def get_WCS_colors():
	from cog_abm.extras.parser import Parser
	import os
	return Parser().parse_environment(
				os.path.join(os.path.dirname(__file__), "330WCS.xml")).stimuli


def get_1269Munsell_chips():
	from cog_abm.extras.parser import Parser
	import os
	return Parser().parse_environment(
				os.path.join(os.path.dirname(__file__), "1269_munsell_chips.xml")).stimuli
