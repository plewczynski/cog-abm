"""
Module providing flow control in simulation
"""
import random
import logging
from itertools import izip
from time import time
import copy
import cPickle
from progressbar import ProgressBar, Percentage, Bar, ETA



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
		#cc = [a.deepcopy() for a in self.agents]
		kr = (iter_num, cc)
		self.statistic.append(kr)
		f = open(str(iter_num)+".pout", "wb")
		cPickle.dump(kr, f)
		f.close()
	
	
	def _choose_agents(self):
		if self.interaction.num_agents() == 2:
			l = random.randint(0, len(self.agents)-1)
			a = self.agents[l]
			b = self.graph.get_random_neighbour(a)
			return [a,b]
		else :
			return [random.choice(self.agents)]
		
	
	def _start_interaction(self, agents):
		self.interaction.interact(*agents)
#		results = self.interaction.interact(*agents)
#		for r, a in izip(results, agents):
#			a.add_inter_result(r)

	
	def _do_iterations(self, num_iter):
		for _ in xrange(num_iter):
			agents = self._choose_agents()
			self._start_interaction(agents)

		

	def run(self, iterations = 1000, dump_freq = 10):
		"""
		Begins simulation.
		
		iterations
		"""
		start_time = time()
		logging.info("Simulation start...")
		
		self.dump_results(0)
		pb = ProgressBar(widgets=[Percentage(), Bar(), ETA()])
		for i in pb(xrange(iterations//dump_freq)):
			self._do_iterations(dump_freq)
			self.dump_results((i+1)*dump_freq)
		
		logging.info("Simulation end. Total time: "+str(time()-start_time))
		return self.statistic
			

	
#	def continue_experiment(self, iterations = 1000, dump_freq = 10):
