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
	environments = {}
	
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
		

	def run(self, iterations = 1000, dump_freq = 10):
		"""
		Begins simulation.
		
		iterations
		"""
		start_time = time()
		logging.info("Simulation start...")
		
		
		self.dump_results(0)

		
		for i in xrange(iterations):
			if self.interaction.num_agents() == 2:
				a = random.choice(self.agents)
				b = self.graph.get_random_neighbour(a)
				r1, r2 = self.interaction.interact(a, b)
				a.add_inter_result(r1)
				b.add_inter_result(r2)
#				(a, b) = random.choice(self.graph.edges())
#				r1, r2 = self.interaction.interact(self.agents[a],  self.agents[b])
#				self.agents[a].add_inter_result(r1)
#				self.agents[b].add_inter_result(r2)
			else :
				a = random.choice(self.agents)
				r = self.interaction.interact(a)
				a.add_inter_result(r)
				
			
			if (i+1) % dump_freq == 0:
				self.dump_results(i+1)
				
		
		
		logging.info("Simulation end. Total time: "+str(time()-start_time))
		return self.statistic
			

	
#	def continue_experiment(self, iterations = 1000, dump_freq = 10):
		

	
