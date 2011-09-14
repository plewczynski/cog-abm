"""
Module providing definition of the Perception class and its concretization:
StimulusColor class.
"""

class Perception(object):
	"""
	Stimulus denoting the single object perceived by agents. Most class in the
	project see this class.
	"""
	
	def to_ML_data(self):
		raise NotImplementedError



class SimplePerception(Perception):
	
	def __init__(self, content):
		self.content = content
	
	
	def to_ML_data(self):
		return self.content.to_ML_data()



class VectorPerception(Perception):
	
	def __init__(self, content):
		"""
		content must be a sequence!
		"""
		self.content = content
	
	
	def to_ML_data(self):
		return self.content

