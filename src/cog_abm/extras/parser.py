"""
Module provides parser for xml documents.
"""
import xml.dom.minidom
from pygraph.readwrite import markup
from cog_abm.core.network import Network
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
		self.interaction_parser_map["DiscriminationGame"] = \
		self.parse_discrimination_game
		self.interaction_parser_map["GuessingGame"] = self.parse_guessing_game
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
		
	def parse_agent(self, agent, network):
		"""
		Parse agent properties when given as DOM object.
		
		@type agent: DOM object
		@param agent: DOM object representing agent.
		
		@type simulation: simulation
		@param simulation: Simulation object
		"""
		#TODO:
		id = self.return_element_if_exist(agent, "id")
		env_name = self.return_element_if_exist(agent, "environment")
		node_name = self.return_element_if_exist(agent, "node_name")
		#sensor = agent.getElementsByTagName("sensor")
		#sensor_type = sensor[0].getElementsByTagName("type")[0].firstChild.dat
		#lrn = agent.getElementsByTagName("classifier")
		#lrn_type = lrn[0].getElementsByTagName("type")[0].firstChild.data
		
		agent = Agent(environment = env_name)
		if network is not None:
			network.add_agent(agent, node_name)
		return agent
		
	def parse_agents(self, source, network):
		"""
		Parse agents when given in xml.

		@type simulation: simulation
		@param simulation: Simulation object
		
		@type source: String
		@param source: XML document for pygraph directory.
		"""
		if source is None:
			return None
		agents = []
		sock = self.build_DOM(source)
		agent_sock = sock.getElementsByTagName("agent")
		for agent in agent_sock:
			agents.append(self.parse_agent(agent, network))
			
		return agents
		
	def parse_environment(self, doc, main_sock = None):
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
		environment = self.environment_parser_map[env_type](env, main_sock) 
		return environment
		
	def parse_graph(self, source):
		"""
		Parse graph when given as pygraph in xml.
		
		@type source: String
		@param source: XML document for pygraph directory.
		
		@rtype: pygraph
		@return: Returns graph from pygraph library.
		"""
		if source is None:
			return None
		with open(source, 'r') as file:
			return Network(markup.read(file.read()))
		
	def parse_simulation(self, source):
		"""
		Parse simulation parameters given in xml document.
		
		@type source: String
		@param source: Simulation XML document directory.
		
		@rtype: Dictionary
		@return: Simulation params created from xml document.
		"""
		if source is None:
			return None
			
		sock = self.build_DOM(source)
		dictionary = {}
		
		dictionary["dump_freq"] = self.return_if_exist(sock, "history", 
		"freq", int)
		dictionary["topology"] = self.parse_graph(self.return_if_exist
		                                          (sock,"network", "source", str))
		
		environments = {}
		envs = sock.getElementsByTagName("environment")
		for env in envs:
			env_name = env.getAttribute("name")
			env_source = env.getAttribute("source")
			environments[env_name] = self.parse_environment(env_source, env)
		
		dictionary ['environments']  = environments
		dictionary["agents"] = self.parse_agents(self.return_if_exist
						(sock,"agents", "source", str), dictionary["topology"])
		
		#inters = sock.getElementsByTagName("interaction")
		inter = self.return_element_if_exist(sock, "interaction", False)
		#for i in inters:
		dictionary.update(self.interaction_parser_map[self.return_if_exist(
					sock, "interaction", "type", str)](inter))

		return dictionary
				
	def parse_munsell_chips(self, chips):
		list = []
		for chip in chips:
			list.append(self.parse_munsell_chip(chip))
		return list
		
	def parse_munsell_chip(self, chip):
		L = float(chip.getElementsByTagName("L")[0].firstChild.data)
		a = float(chip.getElementsByTagName("a")[0].firstChild.data)
		b = float(chip.getElementsByTagName("b")[0].firstChild.data)
		return Color(L, a, b)

	def parse_munsell_environment(self, env, main_sock):
		list_of_stimuli = self.parse_munsell_chips(env.getElementsByTagName
		                                ("munsell_chip"))
		
		params = self.return_element_if_exist(main_sock, "params", False)
		
		chooser = None
		if params is not None:
			dist = self.return_if_exist(params, "distance", "value", float)
			chooser = RandomStimuliChooser(use_distance=True, distance=dist)
		else:
			chooser = RandomStimuliChooser()
		
		return Environment(list_of_stimuli, chooser)
		
	def parse_discrimination_game(self, inter):
		params = self.return_element_if_exist(inter, "params", False)
		if params is None:
			return {}
		dictionary = {"interaction_type":"DG"}
		
		dictionary["num_iter"] = self.return_if_exist(params, "num_iter", 
		"value", int)
		dictionary["context_size"] = self.return_if_exist(params, 
		"context_size", "value", int)
		dictionary["alpha"] = self.return_if_exist(params, "alpha", 
		"value", float)
		dictionary["beta"] = self.return_if_exist(params, "beta", 
		"value", float)
		dictionary["sigma"] = self.return_if_exist(params,
		"inc_category_treshold", "value", float)
		dictionary["inc_category_treshold"] = self.return_if_exist(params,
		"inc_category_treshold", "value", float)
		dictionary["classifier"] = self.return_if_exist(params, "classifier",
													"name", str)
		
		return dictionary
		
	def parse_guessing_game(self, inter):
		params = self.return_element_if_exist(inter, "params", False)
		if params is None:
			return {}
		dictionary = {"interaction_type":"GG"}

		dictionary["num_iter"] = self.return_if_exist(params, 
		"num_iter", "value", int)
		dictionary["context_size"] = self.return_if_exist(params, 
		"context_size", "value", int)
		dictionary["alpha"] = self.return_if_exist(params, "alpha", "value",
												float)
		dictionary["beta"] = self.return_if_exist(params, "beta", 
		"value", float)
		dictionary["sigma"] = self.return_if_exist(params,
		"inc_category_treshold", "value", float)
		dictionary["inc_category_treshold"] = self.return_if_exist(params,
		"inc_category_treshold", "value", float)
		dictionary["classifier"] = self.return_if_exist(params, "classifier",
													"name", str)
		
		return dictionary
		
	def return_if_exist(self, param, name, value, function=None):	
		#print param.getElementsByTagName(name)
		if (len(param.getElementsByTagName(name)) == 0):
			return None
		elif (param.getElementsByTagName(name)[0].hasAttribute(value)):
			if (function is None):
				return param.getElementsByTagName(name)[0].getAttribute(value)
			else:
				return function(param.getElementsByTagName(name)[0].
				                getAttribute(value))
		else:
			return None
	
	def return_element_if_exist(self, sock, name, child = True, function=None):
		if sock is None:
			return None
		elif (len(sock.getElementsByTagName(name)) == 0):
			return None
		else:
			if child is not True:
				return sock.getElementsByTagName(name)[0]
			elif function is None:
				return sock.getElementsByTagName(name)[0].firstChild.data
			else:
				return function(sock.getElementsByTagName(name)[0].
				                firstChild.data)
