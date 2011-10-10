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
	
	ID = 2**30

	def __init__(self, aid = None, state = None, sensor = None, environment = None):
#	def __init__(self, state = None, sensor = None, environment = None):
		if aid is None:
			Agent.ID+=1
			self.id = Agent.ID
		else:
			self.id = aid
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


#	def classify(self, sample):
#		return self.state.classify(sample)


	def sense_and_classify(self, stimulus):
		return self.state.classify(self.sense(stimulus))
		#return self.classify(self.sense(stimulus))


	def __str__(self):
		return "Agent("+str(self.id)+":"+str(self.state)+")"
	
	
	def __eq__(self, other):
		return self.id == other.id


	def __hash__(self):
		return hash(self.id)
	

	def add_inter_result(self, res):
		self.inter_res.append(res)
	
