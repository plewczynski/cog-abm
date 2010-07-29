"""
Module providing flow control in simulation
"""

class Simulation(object):
	"""
	This class defines what happens and when.
	"""
	
	global_environment = None
	environments = []
	
	def __init__(self,  graph = None,  interaction = None):
		self.graph = graph
		self.interaction = interaction
		#self.
		
	def run(self, iterations = 1000):
		"""
		Begins simulation.
		
		iterations
		"""
		for i in range(iterations):
			#whatever
			print i
			
		
		#TODO: should return some history
		return None
	
#	@classmethod
#	def get_global_environment(cls):
#		return cls.global_environment
#	
#	@classmethod
#	def get_all_environments(cls):
#		return cls.environments
	
