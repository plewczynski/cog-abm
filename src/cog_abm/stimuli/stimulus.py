"""
Module providing definition of the Stimulus class and its concretization:
StimulusColor class.
"""
import math

class Stimulus(object):
	"""
	Stimulus denoting the single object perceived by agents. Most class in the
	project see this class.
	"""


class SimpleStimulus(Stimulus):
	
	def __init__(self,  content):
		self.content = content
	
	
	def distance(self, other):
		return self.content.distance(other.content)
	
	
	def __eq__(self, other):
		return self.content == other.content


class VectorStimulus(SimpleStimulus):
	"""
	Class representing stimulus in vector form.
	It also provides euclidean distance for some metrics etc.
	"""
	
	def distance(self, other):
		return math.sqrt(math.fsum(
					[(x-y)**2 for x, y in zip(self.content, other.content)]))
