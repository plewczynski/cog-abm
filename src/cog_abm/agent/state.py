"""
Module provides state and state history for agent.
"""

class AgentState(object):
	"""
	AgentState class.
	
	Agent state is a class that specifies current agent behaviour. It
	provides methods that describe the way agent cooperate with
	percepted stimulus coming from environment. 
	
	@attention: You can redefine or change this class to provide new 
	functionality to an agent. It is recommended to change AgentState or build
	inherited class instead of changing Agent class.
	
	@sort: __init__, clone, clone_state, get_state
	"""
	
	def __init__(self):
		"""
		Initialize an AgentState.
		
		@attention: You should specify type of AgentState. You can add
		new type of agent state by implementing new class and redefining
		this function.
		"""
		self.state = None
	
	def clone(self):
		"""
		Return a copy of whole current AgentState.
		
		@rtype: AgentState
		@return: Return new instance of AgentState.
		"""
		#return self.deepcopy()
		pass
		
	def clone_state(self):
		"""
		Return a copy of current agent low-level state.
		
		@attention: This function does not clone whole instance of AgentState.
		
		@rtype: state
		@return: Return new instance (copy) of low-level state.
		"""
		return self.state.clone()
		
	def get_state(self):
		"""
		Retrun object that represent concrete state.
		
		@rtype: state
		@return: Return object that keeps current information about agent state
		e.g. high-level classifier.
		"""
		return self.state
	
	
	def clean(self, environment, sensor):
		"""
		Alows agent state to clean up before dumping into file
		"""
		pass
		
class StateHistory(object):
	"""
	StateHistory class.
	
	StateHistory class provides a set of states from agent history.
	
	@attention: This class does not keep whole AgentState objects, but 
	low-level states.
	
	@sort: __init__, __len__, add_state, get_state
	"""
	
	def __init__(self, freq = None):
		"""
		Initialize a StateHistory for an agent.
		
		@type  freq: number
		@param freq: Frequency of saving changed states to the history.
		
		@attention: You should specify frequency of saving states to history.
		In other case all states will be saved.
		"""
		if (freq is None):
			self.freq = 1
		else:
			self.freq = freq
		self.counter = self.freq		#counter used to skip states
		self.states = []		#list of states
	
	def __len__(self):
		"""
		Return the number of states in the history when requested by len().

		@rtype:  number
		@return: Size of the hypergraph.
		"""
		return len(self.states)
	
	def add_state(self, state):
		"""
		Add state to state history.
		
		@type state: state
		@param state: Current low-level state of agent.
		"""
		if (self.counter == self.freq):
			self.states.append(state.clone_state())
			self.counter = 1
		else:	#skips state and increases counter
			self.counter += 1
	
	def get_state(self, number):
		"""
		Return chosen state from history.
		
		@type number: number
		@param number: Chronological position of state in history.
		
		@rtype: state
		@return: Chosen state from agent history.
		"""
		return self.states[number]



