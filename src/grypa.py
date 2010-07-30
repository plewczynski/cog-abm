from pygraph.classes.graph import graph
from pygraph.algorithms.generators import *
from cog_abm.core.simulation import *
from cog_abm.agent.state import *
from cog_abm.core.agent import *
import random

#import sys
#print sys.path

# powinno po interakcji dziedziczyc, ale ze je nie ma..
class Kontakt(object):
	
	@classmethod
	def num_agents(cls):
		return 2
		
	@staticmethod
	def get_state(ags):
		return ags.stan
		
	@classmethod
	def interact(cls, agents):
		
		for a in agents:
			a.accept_fun(lambda x: x.update_state())
		
		zarazacze = \
			[a for a in agents \
				if a.accept_fun(Kontakt.get_state) == "ZA"]
		
		if len(zarazacze)>0:
			for a in agents:
				s = a.accept_fun(lambda x: x.zarazaja())



class GrypowyAgentState(AgentState):
	
	def __init__(self, chory=False):
		if chory:
			self.stan = "ZA"
		else :
			self.stan = "ZD"
		self.dni_choroby = 0
		
	def zarazaja(self):
		if self.stan == "ZD" and random.choice([True, False]):
			self.stan = "ZA"
			self.dni_choroby = 0
	
	def update_state(self):
		if self.stan == "CH" or self.stan == "ZA":
			self.dni_choroby += 1
		
		if self.stan == "ZA" and self.dni_choroby>3:
			self.stan = "CH"
			self.dni_choroby = 0
			
		if self.stan == "CH" and self.dni_choroby >2:
			self.stan = "ZD"
			self.dni_choroby = 0
			
	def __str__(self):
		return "GrypowyAgent: "+self.stan




# wlasciwa czesc
NUM = 20
il_chorych = 3

agents = [Agent(GrypowyAgentState(True)) for i in range(il_chorych)] \
		+[Agent(GrypowyAgentState()) for i in range(NUM-il_chorych)]

graf = generate(NUM, 40)



sim = Simulation(graf,  Kontakt(),  agents)

sim.run(100)

print graf.nodes()

