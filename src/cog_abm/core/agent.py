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
	
#	def __init__(self, id = None, state = None, sensor = None, environment = None):
	def __init__(self, state = None, sensor = None, environment = None):
		self.id = id
		self.sensor = sensor
		self.state = state
		self.env = environment
		self.inter_res = []
	
	def set_state(self, state):
		self.state = state

	def set_sensor(self, sensor):
		self.sensor = sensor
		
	def get_environment(self):
		"""
		Gives environment where given agent "lives"
		"""
		if self.env is None:
			return Simulation.global_environment
			
		return Simulation.environments[self.env]
		

	environment = property(get_environment)
	
	
	def sense(self,  stimulus):
		"""
		Returns list with sensors perception of given stimulus
		"""
		return self.sensor.sense(stimulus)
	
	
	def classify(self, stimulus):
		return self.state.classify(self.sense(stimulus))
		
		
	def __str__(self):
		return self.state.__str__()
	
	
	def add_inter_result(self, res):
		self.inter_res.append(res)
