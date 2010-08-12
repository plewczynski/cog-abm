"""
Module providing definition of the Perception class and its concretization:
StimulusColor class.
"""

class Perception(object):
	"""
	Stimulus denoting the single object perceived by agents. Most class in the
	project see this class.
	"""


class SimplePerception(Perception):
	
	def __init__(self,  content):
		self.content = content
	
	
	def to_ML_data(self):
		return self.content.to_ML_data()
