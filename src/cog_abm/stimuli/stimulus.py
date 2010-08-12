"""
Module providing definition of the Stimulus class and its concretization:
StimulusColor class.
"""


class Stimulus(object):
	"""
	Stimulus denoting the single object perceived by agents. Most class in the
	project see this class.
	"""


class SimpleStimulus(Stimulus):
	
	def __init__(self,  content):
		self.content = content
