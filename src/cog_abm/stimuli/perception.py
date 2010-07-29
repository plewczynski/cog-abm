"""
Module providing definition of the Perception class and its concretization:
StimulusColor class.
"""

class Perception(object):
	"""
	Stimulus denoting the single object perceived by agents. Most class in the
	project see this class.
	"""

class PerceptionColor(Perception):
	"""
	StimulusColor makes concretization of Stimulus. Encapsulates Color class
	"""
	
	def __init__(self, content):
		"""
		Initialisation of StimulusColor takes content and writes it.
		
		@type  content: Color
		@param content: Color instance
		"""
		self.color = content

