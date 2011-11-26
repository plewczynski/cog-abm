"""
This module implements Steels exepriment.
"""
import math
import sys
import random
from steels import metrics
sys.path.append("../")

from cog_abm.extras.tools import *
from cog_abm.core.interaction import Interaction

from cog_abm.ML.conv_classif_str import *
from cog_abm.ML.core import Classifier

from cog_abm.agent.sensor import SimpleSensor


class ReactiveUnit(object):
	""" Reactive units are used in adaptive networks
	"""
	
	def_sigma = 10.
	
	def __init__(self, central_value, sigma = None):
		self.central_value = [float(x) for x in central_value]
		self.sigma = float(def_value(sigma, ReactiveUnit.def_sigma))
		self.mdub_sqr_sig = (-2.)*(self.sigma**2.)
		
	
	
	def value_for(self, x):
		""" Calculate reaction for given vector
		"""
		fsum = math.fsum( 
			imap(lambda (xi, mi):(xi-mi)**2., izip(x, self.central_value)))

		return math.exp(fsum / self.mdub_sqr_sig)
	
	
	def __eq__(self,  other):
		if isinstance(other,  ReactiveUnit):
			return other.central_value == self.central_value
		else:
			return False
	
	

class AdaptiveNetwork(object):
	""" Adaptive network is some kind of classifier
	"""
	
	def_alpha = 0.1
	def_beta = 1.
	
	def __init__(self,  reactive_units = None, alpha = None, beta = None):
		""" Must be with weights !
		"""
		self.units = def_value(reactive_units, [])
		self.alpha = def_value(alpha, AdaptiveNetwork.def_alpha)
		self.beta = def_value(beta, AdaptiveNetwork.def_beta)
	
	
	def _index_of(self, unit):
		""" Finds index of given unit.
		Returns -1 if there is no such unit in this network
		"""
		for i, (u, _) in enumerate(self.units):
			if u == unit:
				return i
		return -1
	
	
	def add_reactive_unit(self,  unit,  weight = 1.):
		index = self._index_of(unit)
		if index == -1:
			self.units.append((unit, weight))
		else:
			self.units[index] = (unit, weight)
	
	
	def reaction(self,  data):
		return math.fsum([w*u.value_for(data) for u,  w in self.units])
	
	
	def _update_units(self,  fun):
		tmp = [fun(u, w) for u, w in self.units]
		self.units = filter(lambda x: x is not None,  tmp)

	
	def remove_low_units(self,  threshold = 0.1**30):
		self.units = [(u, w) for u, w in self.units if w >= threshold]
	
	
	def increase_sample(self, sample):
		self._update_units(lambda u, w:
						(u, min(1.,w+float(self.beta)*u.value_for(sample))))
					# because we don't want to exceed 1
	
	
	#TODO: rewrite it to be in time O(1)
	def forgetting(self):
		self._update_units(lambda u, w: (u, self.alpha*w))
#		self.remove_low_units(0.1**50)
#		TODO: think about ^^^^^
	
	
	
	
class SteelsClassifier(Classifier):
	
	def __init__(self):
		self.categories = {}
		self.new_category_id = 0
	
	
	def add_category(self, sample = None, class_id = None):
		if class_id is None:
			class_id = self.new_category_id
			self.new_category_id += 1
			adaptive_network = AdaptiveNetwork()
		
		else:
			adaptive_network = self.categories[class_id]
		
		if sample is not None:
			adaptive_network.add_reactive_unit(ReactiveUnit(sample.get_values()))
		
		self.categories[class_id] = adaptive_network
		return class_id
	
	
	def del_category(self,  category_id):
		self.categories.pop(category_id, None)

	
	def classify(self, sample):
		if len(self.categories) == 0:
			return None
		values = sample.get_values()
		return max(self.categories.iteritems(), key = 
		           lambda kr: kr[1].reaction(values))[0]
	
	
	def increase_samples_category(self, sample):
		category_id = self.classify(sample)
		values = sample.get_values()
		self.categories[category_id].increase_sample(values)
	
	
	def forgetting(self):
		for _, an in self.categories.iteritems():
			an.forgetting()
	
	
	def sample_strength(self, category_id, sample):
		return self.categories[category_id].reaction(sample.get_values())


def convert_to_classifier_steels(classifier):
	#print 'classifier: ', classifier#classifier = def_value(None, SteelsClassifier)
	if classifier == "SteelsClassifier":
		return SteelsClassifier, []
	else:
		return  convert_to_classifier(classifier)


from metrics import DS_A

class DiscriminationGame(Interaction):
	
	def_inc_category_treshold = 0.95
	
	def __init__(self, context_len = 4, inc_category_treshold = None):
		self.context_len = context_len
		self.inc_category_treshold = def_value(inc_category_treshold, 
								DiscriminationGame.def_inc_category_treshold)
	
	
	def num_agents(self):
		return 2
	
	
	def save_result(self, agent, result):
		agent.add_payoff("DG", int(result))
	
	
	def disc_game(self, agent, context, topic):

		ctopic = agent.sense_and_classify(topic)
		# no problem if ctopic is None => count>1 so it will add new category

		ccontext = [agent.sense_and_classify(c) for c in context]
		count = ccontext.count(ctopic)

		return (count == 1, ctopic)

	
	def learning_after(self, agent, topic, succ, ctopic = None):

		succ_rate = DS_A(agent)
		sensed_topic = agent.sense(topic)
		
		if succ:
			agent.state.classifier.increase_samples_category(sensed_topic)
		elif succ_rate >= self.inc_category_treshold:
			#agent.state.incrase_samples_category(topic)
			if ctopic is None:
				ctopic = agent.state.classifier.classify(sensed_topic)
			agent.state.classifier.add_category(sensed_topic, ctopic)

		else:
			agent.state.classifier.add_category(sensed_topic)
		
		# lower strength of memory
		agent.state.classifier.forgetting()
		
	
	def play_with_learning(self, agent, context, topic):

		succ, ctopic = \
				self.disc_game(agent, context, topic)
		
		self.learning_after(agent, topic, succ, ctopic)
		
		return succ, ctopic, topic, context
	
	
	def play_save(self, agent, context, topic):
		succ, ctopic = self.disc_game(agent, context, topic)
		self.save_result(agent, succ)
		return succ, ctopic


	def play_learn_save(self, agent, context, topic):
		succ, ctopic, topic, context = \
			self.play_with_learning(agent, context, topic)
		
		#agent.add_inter_result(("DG", succ))
		self.save_result(agent, succ)
		return succ, ctopic, topic, context 
		
	def interact(self, agent1, agent2):
		
		env = agent1.get_environment()
		context = env.get_random_stimuli(self.context_len)
		
		topic = random.choice(context)
		succ1, _, _, _ = self.play_with_learning(agent1, context, topic)
		succ2, _, _, _ = self.play_with_learning(agent2, context, topic)
		self.save_result(agent1, succ1)
		self.save_result(agent2, succ2)
		return (("DG", succ1), ("DG", succ2))



class GuessingGame(Interaction):
	
	def __init__(self, disc_game = None, context_size = None):
		if disc_game is None:
			disc_game = DiscriminationGame()
			if context_size is not None:
				disc_game.context_len = context_size
		
		self.disc_game = disc_game


	def num_agents(self):
		return 2


	def save_result(self, agent, result):
		agent.add_payoff("GG", int(result))
	

	def learning_after(self, speaker, hearer, succ, sp_topic, he_topic, word, topic):
		if succ:
			speaker.state.lexicon.increase_word(sp_topic, word)
			hearer.state.lexicon.increase_category(he_topic, word)
			# z opisu w 4.3 pierwszy paragraf
			
			for a in [speaker, hearer]:
				a.state.classifier.increase_samples_category(a.sense(topic))
		else:

			speaker.state.lexicon.decrease(sp_topic, word)
			hearer.state.lexicon.decrease(he_topic, word)
			#domniemania z punktu 6 w ostatnim podrozdziale 2
			#hearer.state.classifier
			self.disc_game.learning_after(hearer, topic, False)
		

	def guess_game(self, speaker, hearer):

		env = speaker.get_environment()
		context = env.get_random_stimuli(self.disc_game.context_len)

		topic = random.choice(context)

		succ, spctopic = self.disc_game.play_save(speaker, context, topic)

		if not succ:
			self.disc_game.learning_after(speaker, topic, succ, spctopic)
			return False

		f = speaker.state.word_for(spctopic)
		if f is None:
			f = speaker.state.lexicon.add_element(spctopic)


		#step 4
		hcategory = hearer.state.category_for(f)
#		print "hearers category for "+str(f)+" is "+str(hcategory)

		if hcategory is None:
			#fail in game - hearer doesn't know the word f

			succ, hectopic = self.disc_game.play_save(hearer, context, topic)
			#TODO Q: should hearer also learn?
			if succ:
				#print " ale dyskryminuje topic "+str(ctopic)
				#???: the word form f is associated with category ...??
				hearer.state.lexicon.add_element(hectopic, f)

			else:
				#print " i go nie dyskryminuje"

				#class_id = hearer.state.classifier.add_category(
				#                                                hearer.sense(topic).to_ML_data())
				#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
				self.disc_game.learning_after(hearer, topic, succ, hectopic)
				class_id = hearer.sense_and_classify(topic)
				hearer.state.lexicon.add_element(class_id, f)

			# disc_game samo stworzy ew kategorie?

			return False


		hsf = argmax(lambda c: hearer.state.sample_strength(hcategory, 
												hearer.sense(c)), context)[1]

		#step 6

		succ = hsf == topic
		hectopic = hearer.sense_and_classify(hsf)
		#print "hearer_topic: "+str(hectopic)+"  hsf: "+str(hsf)+"   succ: "+str(succ)
#		self.learning_after(speaker, hearer, succ, spctopic, hectopic, f, topic)
		self.learning_after(speaker, hearer, succ, spctopic, hcategory, f, topic)

		return succ
		

	def interact(self, speaker, hearer):
		r = self.guess_game(speaker, hearer)
		self.save_result(speaker, r)
		self.save_result(hearer, r)
		return (("GG", r), ("GG", r))



#class SteelsAgentState(AgentState):
class SteelsAgentState(object):

	def __init__(self, classifier):
		self.classifier = classifier


	def classify(self, sample):
		return self.classifier.classify(sample)


	def sample_strength(self, category, sample):
		return self.classifier.sample_strength(category, sample)



class SteelsAgentStateWithLexicon(SteelsAgentState):
	
	def __init__(self, classifier, initial_lexicon = None):
		super(SteelsAgentStateWithLexicon, self).__init__(classifier)
		from cog_abm.extras.lexicon import Lexicon

		if initial_lexicon is None:
			initial_lexicon = Lexicon()
		self.lexicon = initial_lexicon
	
	
	def category_for(self, word):
		return self.lexicon.category_for(word)
	
	def word_for(self, category):
		return self.lexicon.word_for(category)


#Steels experiment main part

def steels_uniwersal_basic_experiment(num_iter, agents, environments, interaction,
			classifier = SteelsClassifier, topology = None,
			inc_category_treshold = None, dump_freq = 50, stimuli = None):
				
	from cog_abm.core import Environment, Simulation
	from pygraph.algorithms.generators import generate

	num_agents = len(agents)
	topology = def_value(topology, 
	                     generate(num_agents, num_agents*(num_agents-1)/2))
	
#	if stimuli == None:
#		stimuli = def_value(None, default_stimuli())
	
	if inc_category_treshold is not None:
		interaction.__class__.def_inc_category_treshold = inc_category_treshold
		
	env = Environment(stimuli, True)
	for key in environments.keys():
			Simulation.environments[key] = Environment(environments[key].stimuli, True, 50.)
	#TODO: think about this all...
	glob = Simulation.environments["global"]

		
	Simulation.global_environment = def_value(glob , env)

	s = Simulation(topology, interaction, agents)
	res = s.run(num_iter, dump_freq)
	
	return res




def steels_basic_experiment_DG(inc_category_treshold = 0.95, classifier = None, 
			environments = None, interaction_type="DG", beta = 1., context_size = 4,
			agents = None, dump_freq = 50, alpha = 0.1, sigma = 1., num_iter = 1000, topology = None, stimuli = None):
	
	environments = def_value(environments, {})
	classifier, classif_arg = convert_to_classifier_steels(classifier)

	# FIX THIS !!
	for agent in agents:
		agent.set_state(SteelsAgentState(classifier(*classif_arg)))
		agent.set_sensor(SimpleSensor())
		agent.set_fitness_measure("DG", metrics.get_DS_measure())
	
	AdaptiveNetwork.def_alpha = float(alpha)
	AdaptiveNetwork.def_beta = float(beta)
	ReactiveUnit.def_sigma = float(sigma)
	DiscriminationGame.def_inc_category_treshold = float(inc_category_treshold)
	
	return steels_uniwersal_basic_experiment(num_iter, agents, environments, 
						DiscriminationGame(context_size), topology = topology, 
						dump_freq = dump_freq, stimuli = stimuli)


def steels_basic_experiment_GG(inc_category_treshold = 0.95, classifier = None, 
			environments = None, interaction_type="GG", beta = 1., context_size = 4,
			agents = None, dump_freq = 50, alpha = 0.1, sigma = 1., num_iter = 1000, topology = None):

	environments = def_value(environments, {})
	classifier, classif_arg = convert_to_classifier_steels(classifier)
	#agents = [Agent(SteelsAgentStateWithLexicon(classifier()), SimpleSensor())\

	# FIX THIS !!
	classif_arg = def_value(classif_arg, [])
	for agent in agents:
		agent.set_state(SteelsAgentStateWithLexicon(classifier(*classif_arg)))
		agent.set_sensor(SimpleSensor())
		agent.set_fitness_measure("DG", metrics.get_DS_measure())
		agent.set_fitness_measure("GG", metrics.get_CS_fitness())
	
	AdaptiveNetwork.def_alpha = float(alpha)
	AdaptiveNetwork.def_beta = float(beta)
	ReactiveUnit.def_sigma = float(sigma)
	DiscriminationGame.def_inc_category_treshold = float(inc_category_treshold)
	
	return steels_uniwersal_basic_experiment(num_iter, agents, environments, 
						GuessingGame(None, context_size), topology = topology, 
						dump_freq = dump_freq)


