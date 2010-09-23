"""
Module represents agent allocation in cognitive system.
"""
from pygraph.classes.graph import graph
from random import choice

class Node(object):
	"""
	Node class.
	
	Node class describes one node of network. It can be considered as a set 
	of agents.
	
	@sort: __init__, __len__, add_agent, get_agents
	"""
		
	def __init__(self, name, agents = None):
		"""
		Initialize one node.
		
		@type name: String
		@param name: Unique name of node.
		
		@type agents: list
		@param agents: List of agents assigned to this node.
		"""
		self.name = name 
		self.agents = []
		if (agents is not None):
			self.agents.append(agents)
				
	def __len__(self):
		"""
		Return number of agents assigned.
		
		@rtype: number
		@return: Number of agents.
		"""
		return len(self.agents)
		
	def add_agent(self, agent):
		"""
		Add agent to the node.
		
		@type agent: agent
		@param agent: Agent to be added to the node.
		"""
		self.agents.append(agent)
		
	def get_agents(self):
		"""
		Return all agents assigned to this node.
		
		@rtype: list
		@return: Return list of agents.
		"""
		return self.agents
		
		
class Network(object):
	"""
	Network class.
	
	Network is a class that describes geographical allocation of agent sets.
	
	@attention: Network class uses graph from pygraph library.
	
	@sort: __init__, __len__, add_agent, get_neighbour_nodes, 
	get_random_neighbour, get_random_neighbours
	"""
		
	def __init__(self, pygraph):
		"""
		Initialize network with given graph from pygraph library.
		
		@type graph: graph
		@param graph: Initializing graph.
		"""
		self.nodes = {} #dictionary node_name -> node
		self.agents = {} #dictionary agent -> node_name
		self.graph = pygraph
		for node in self.graph.nodes():
			self.nodes[node] = Node(node)
			
	def __len__(self):
		"""
		Return number of nodes in this network.
		
		@rtype: number
		@return: Number of nodes.
		"""
		return len(self.nodes)
	
	#UNCOMMENT jezeli zmieniamy ze agent moze nalezec do kilku wezlow
	# wtedy moze pojawic sie problem ze slownikiem ?
	#def add_agent(self, agent, node_name_list):
	#	"""
	#	Add agent to the network. 
	#	
	#	@attention: Every agent can be assigned to many nodes.
	#	
	#	@type agent: agent
	#	@param agent: Agent to be added to the network.
	#	
	#	@type node_name_list: list
	#	@param node_name_list: List of node names that agent has to be 
	#	assigned to.
	#	"""
	#	for node_name in node_name_list:
	#		self.add_agent(agent, node_name)
	
	def add_agent(self, agent, node_name, agent_name = None):
		"""
		Add agent to the node of network. 

		@attention: It is required to specify agent name if Agent is 
		non-hashable object.
		
		@type agent: agent
		@param agent: Agent to be added to the network.
		
		@type agent: String
		@param agent: Optional name, identifier of Agent.
		
		@type node_name: string
		@param node_name_list: Name of node that agent has to be assigned to.
		"""
		self.nodes[node_name].add_agent(agent)
		
		if (agent_name is None):
			self.agents[agent] = node_name
		else:
			self.agents[agent_name] = node_name
		
	def get_neighbour_nodes(self, node_name):
		"""
		Return list of node names that are adjacent to the given node.
		
		@type node_name: String
		@param node_name: Node name.
		
		@rtype: list
		@return: List of node names that are neighbours to the given node.
		"""
		return self.graph.neighbors(node_name)
	
	def get_random_neighbour(self, agent_name):
		"""
		Return randomly chosen neighbour agent to the given agent.
		
		@type agent: String
		@param agent: Agent asking for neighbour.
		
		@rtype: agent
		@param: Agents that is adjacent to the given agent.
		"""
		return choice(self.get_random_neighbours(agent_name))
		
	def get_random_neighbours(self, agent_name):
		"""
		Return randomly chosen set of neighbour agents to the given agent.
		
		@attention: This function does not return random set of agents from all
		adjacent agents. Adjacent node (to the agent node) will be chosen 
		randomly from set of adjacent nodes. All agents assigned to this node 
		will be returned.
		
		@type agent: String
		@param agent: Agent asking for neighbours.
		
		@rtype: list
		@param: List of agents that are neighbours to the given agent.
		"""
		#TODO: wyjatki jezeli nie ma takiego agenta i jezeli odosobniony wtedy
		#choice nie dziala na pustym zbiorze
		#jezeli wylosowany wezel pusty ... 
		agent_node_name = self.agents[agent_name]
		node_name = choice(self.get_neighbour_nodes(agent_node_name))
		return self.nodes[node_name].get_agents()
