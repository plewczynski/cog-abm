"""
Module provides parser for xml documents.
"""
import urllib
import xml.dom.minidom
import sys
from pygraph.readwrite import markup
from cog_abm.core.network import *
from cog_abm.core.agent import *
from cog_abm.core.environment import *
from cog_abm.extras.color import Color

class Parser(object):
	"""
	Parser class.
	
	Parser provides methods used to handle simulation input when given in xml.
	
	@sort: __init__, open_document, parse_agent, parse_agents, parse_graph, 
	parse_param
	"""
	
	def __init__(self):
		"""
		Initialize parser.
		"""
		self.init_environment_dictionary()
		self.init_interaction_dictionary()

	def init_environment_dictionary(self):
		self.environment_parser_map = {}
		self.environment_parser_map["CIELab"] = self.parse_munsell_environment
	
	def init_interaction_dictionary(self):
		self.interaction_parser_map = {}
		self.interaction_parser_map["1"] = self.parse_discrimination_game
		#self.interaction_parser_map["2"] = self.parse_guessing_game
		#self.interaction_parser_map["3"] = self.parse_genetic_game
		
	def build_DOM(self, source):
		"""
		Open document from source and build DOM tree-structure.
		
		@type source: String
		@param source: XML document directory.
		
		@rtype: DOM tree
		@return: Returns DOM tree created from XML document.
		"""
		with open(source, 'r') as file:
			sock = xml.dom.minidom.parse(file)
			return sock
		
	def parse_agent(self, agent, simulation):
		"""
		Parse agent properties when given as DOM object.
		
		@type agent: DOM object
		@param agent: DOM object representing agent.
		
		@type simulation: simulation
		@param simulation: Simulation object
		"""
		id = agent.getElementsByTagName("id")[0].firstChild.data
		env_name = agent.getElementsByTagName("environment")[0].firstChild.data
		node_name = agent.getElementsByTagName("node_name")[0].firstChild.data
		sensor = agent.getElementsByTagName("sensor")
		sensor_type = sensor[0].getElementsByTagName("type")[0].firstChild.data
		lrn = agent.getElementsByTagName("learning_method")
		lrn_type = lrn[0].getElementsByTagName("type")[0].firstChild.data
		
		simulation.agents.append(Agent(id, simulation.environments[env_name], 
		                               lrn_type, sensor_type, None))
		simulation.network.add_agent(simulation.agents[-1], node_name, id)
	
	def parse_agents(self, source, simulation):
		"""
		Parse agents when given in xml.

		@type simulation: simulation
		@param simulation: Simulation object
		
		@type source: String
		@param source: XML document for pygraph directory.
		"""
		sock = self.build_DOM(source)
		agents = sock.getElementsByTagName("agent")
		for agent in agents:
			self.parse_agent(agent, simulation)
		
	def parse_environment(self, doc):
		"""
		Parse environment parameters given in xml document.
		
		@type doc: String
		@param doc: XML document directory.
		
		@rtype: Environment
		@return: Parsed environment
		"""
		sock = self.build_DOM(doc)
		env = sock.firstChild
		env_type = env.getAttribute("type")
		list_of_stimuli = self.environment_parser_map[env_type](env) 
		return Environment(list_of_stimuli)
		
	def parse_graph(self, source):
		"""
		Parse graph when given as pygraph in xml.
		
		@type source: String
		@param source: XML document for pygraph directory.
		
		@rtype: pygraph
		@return: Returns graph from pygraph library.
		"""
		with open(source, 'r') as file:
			return Network(markup.read(file.read()))
		
	def parse_simulation(self, source, simulation):
		"""
		Parse simulation parameters given in xml document.
		
		@type source: String
		@param source: Simulation XML document directory.
		
		@type simulation: Simulation
		@param simulation: Simulation object created from xml document.
		"""
		sock = self.build_DOM(source)
		
		inters = sock.getElementsByTagName("interaction")
		for i in inters:
			#simulation.add_interaction(inter.getAttribute("type"))
			simulation.interactions[1] = 1
		
		freq = sock.getElementsByTagName("history")[0].getAttribute("freq")
		if (sock.getElementsByTagName("network")[0].hasAttribute("source")):
			net_source = sock.getElementsByTagName("network")[0].getAttribute("source")
			simulation.network = self.parse_graph(net_source)
			
		envs = sock.getElementsByTagName("environment")
		for env in envs:
			env_name = env.getAttribute("name")
			env_source = env.getAttribute("source")
			simulation.environments[env_name] = self.parse_environment(env_source)
	
		agents_source = sock.getElementsByTagName("agents")[0].getAttribute("source")
		self.parse_agents(net_source, simulation)
		
	def parse_munsell_chips(self, chips):
		list = []
		for chip in chips:
			list.append(self.parse_munsell_chip(chip))
		return list
		
	def parse_munsell_chip(self, chip):
		#hue = chip.getElementsByTagName("hue")[0].firstChild.data
		#value = float(chip.getElementsByTagName("value")[0].firstChild.data)
		#chroma = int(chip.getElementsByTagName("chroma")[0].firstChild.data)
		L = float(chip.getElementsByTagName("L")[0].firstChild.data)
		a = float(chip.getElementsByTagName("a")[0].firstChild.data)
		b = float(chip.getElementsByTagName("b")[0].firstChild.data)
		#return MunsellColor(hue, value, chroma, L, a, b)
		return Color(L, a, b)

	def parse_munsell_environment(self, env):
		return self.parse_munsell_chips(env.getElementsByTagName
		                                ("munsell_chip"))
		
	def parse_discrimination_game(self, interaction):
		pass
		
