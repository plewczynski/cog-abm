"""
Module providing flow control in simulation
"""
import random

class Simulation(object):
	"""
	This class defines what happens and when.
	"""
	
	global_environment = None
	environments = []
	
	def __init__(self,  graph = None,  interaction = None,  agents = None):
		self.graph = graph
		self.interaction = interaction
		self.agents = agents
		#self.
		
	def run(self, iterations = 1000):
		"""
		Begins simulation.
		
		iterations
		"""
		n = len(self.agents)
		for i in range(iterations):
			if self.interaction.num_agents() == 2:
				(a, b) = random.choice(self.graph.edges())
				agents = [self.agents[a], self.agents[b]]
			else :
				pass
			self.interaction.interact(agents)
			
			for i in range(n):
				print "A["+str(i)+"]="+ self.agents[i].state.stan+ " |", 
			
			def counter(stan, w, a):
				if a.state.stan == stan:
					return w+1
				else:
					return w
				
			zar = reduce(lambda x, a:counter("ZA", x, a), self.agents,  0)
			cho = reduce(lambda x, a:counter("CH", x, a), self.agents,  0)
			zdr = reduce(lambda x, a:counter("ZD", x, a), self.agents,  0)
			print "ZA:"+str(zar)+"  CH: "+str(cho)+"  ZD: "+str(zdr)
			
		
		#TODO: should return some history
		return None
	
#	@classmethod
#	def get_global_environment(cls):
#		return cls.global_environment
#	
#	@classmethod
#	def get_all_environments(cls):
#		return cls.environments
	
