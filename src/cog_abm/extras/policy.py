import random

class Policy(object):

	def __init__(self):
		self.category_actions = {}


	def _get_new_action_data(self):
		raise NotImplementedError


	def _get_action_vector(self, category):
		action_vector = self.category_actions.get(category)
		if action_vector is None:
			action_vector = self._get_new_action_data()
			self.category_actions[category] = action_vector
		
		return action_vector
	

	def get_action(self, category):
		return self._get_action_vector(category).get_action()


	def add_result(self, category, action, payoff):
		self._get_action_vector(category).add_result(action, payoff)




class StatisticPolicy(Policy):

	class ActionData(object):

		def __init__(self):
			self.sum = 0.
			self.ssum = 0.
			self.count = 0


		def add_value(self, value):
			self.sum += value
			self.ssum += value * value
			self.count += 1
		
		def __str__(self):
			return "sum: %f ssum: %f count: %i" % \
				(self.sum, self.ssum, self.count)


	class ActionsVector(object):

		def __init__(self, random_factor = None):
			self.actions = {}
			self.leadingAction = None
			if random_factor is None:
				self.random_factor = 0.1
			else:
				self.random_factor = random_factor


		def get_action(self):
			r = random.random()
			if r<self.random_factor and self.leadingAction is not None:
				return random.choice(self.actions.keys())

			return self.leadingAction


		def add_result(self, action, payoff):
			if action not in self.actions.keys():
				self.actions[action] = StatisticPolicy.ActionData()

			self.actions[action].add_value(payoff)
			
			if self.leadingAction is None or \
					self.actions[self.leadingAction].sum < self.actions[action].sum:
				self.leadingAction = action



	def __init__(self, random_factor = None):
		super(StatisticPolicy, self).__init__()
		self.random_factor = random_factor


	def _get_new_action_data(self):
		return StatisticPolicy.ActionsVector(self.random_factor)


