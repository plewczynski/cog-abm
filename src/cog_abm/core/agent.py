"""
Module implementing agent in our system
"""

from cog_abm.core.simulation import Simulation

class Agent(object):
	"""
	Class representing agent in our system.
	
	In most cases you shouldn't change or redefine this class. 
	There is special class for that: AgentState
	"""
	
	def __init__(self, state, sensor = None, environment = None):
#		if sensors is None:
#			sensors = []
		self.sensor = sensor
		self.state = state
		self.env = environment
	
	
	def get_environment(self):
		"""
		Gives environment where given agent "lives"
		"""
		if self.env is None:
			return Simulation.global_environment
			
		return self.env
		

	environment = property(get_environment)
	
	
	def sense(self,  stimulus):
		"""
		Returns list with sensors perception of given stimulus
		"""
#		return [sensor.sense(stimulus) for sensor in self.sensors]
		return self.sensor.sense(stimulus)
	
	
	def classify(self, stimulus):
		return self.state.classify(self.sense(stimulus))
		
		
	def __str__(self):
		return self.state.__str__()
