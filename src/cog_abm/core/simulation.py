"""
Module providing flow control in simulation
"""
import random
import logging
from time import time
import copy
import cPickle


class Simulation(object):
	"""
	This class defines what happens and when.
	"""
	
	global_environment = None
	environments = []
	
	def __init__(self,  graph = None,  interaction = None,  agents = None):
		self.graph = graph
		self.interaction = interaction
		self.agents = tuple(agents)
		self.statistic = []
		#self.
	

	def dump_results(self, iter_num):
		cc = copy.deepcopy(self.agents)
		kr = (iter_num, cc)
		self.statistic.append(kr)
		f = open(str(iter_num)+".pout", "wb")
		cPickle.dump(kr, f)
		f.close()
		

	def run(self, iterations = 1000, co_ile = 10):
		"""
		Begins simulation.
		
		iterations
		"""
		start_time = time()
		logging.info("Simulation start...")
		

		n = len(self.agents)
		
		self.dump_results(0)
		
		for i in xrange(iterations):
			if self.interaction.num_agents() == 2:
				(a, b) = random.choice(self.graph.edges())
				self.interaction.interact(self.agents[a],  self.agents[b])
			else :
				self.interaction.interact(random.choice(self.agents))
			
			if (i+1) % co_ile == 0:
				self.dump_results(i+1)
				
		
		
		logging.info("Simulation end. Total time: "+str(time()-start_time))
		return self.statistic
			

	

	
