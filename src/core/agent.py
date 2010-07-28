"""
Module implementing agent in our system
"""

from simulation import Simulation

class Agent(object):
	"""
	Class representing agent in our system.
	
	In most cases you shouldn't change or redefine this class. 
	There is special class for that: AgentState
	"""
	
	def __init__(self, state, sensors = None):
		if sensors is None:
			sensors = []
		self.sensors = sensors
		self.state = state
	
	
	def get_environment(self):
		"""
		Gives environment where given agent "lives"
		"""
		if self.environment is None:
			return Simulation.global_environment
			
		return self.environment
		

	environment = property(get_environment)
	
	
	def sense(self,  stimulus):
		"""
		Returns list with sensors perception of given stimulus
		"""
		return [sensor.sense(stimulus) for sensor in self.sensors]
	
	
	def accept_v(self, vobj):
		return vobj.do(self.state)
	
	
	def accept_fun(self,  fun):
		return fun(self.state)
	
	
	def accept_v_and_sense(self, vobj, stimulus):
		return vobj.do(self.state, self.sense(stimulus))


	def accept_fun_and_sense(self, fun,  stimulus):
		return fun(self.state, self.sense(stimulus))
