from single_classif import *
import simple_classif as smpl#needed in convertion method
import direct_classif as dircl#needed in convertion method

sys.path.append("../")
from cog_abm.extras.abstract_meth import *

class MultiClassifier(object):
	"""Base abstract class for all classifiers that use many single classifiers.
	"""
	def __init__(self, simple_classifier_type):
		"""@param simple_classifier_type: classifier wrapper used in this specific multi classifier. Has to inherit from SimpleClassifier.
		"""
		self.categories = {}
		self.new_category_id = 0
		self.classif = simple_classifier_type
	
	def add_category(self, sample, context, class_id = None):#nie moze byc context None!
		"""Adds a new category to the categories. Called in discrimination game.
		"""
		if class_id is None:
			class_id = self.new_category_id
			self.new_category_id += 1
			tempClassifier = SingleClassifier(self.classif)
		else:
			tempClassifier = self.categories[class_id]
		
		if sample is not None:
			tempClassifier.add_positives([sample])
		
		if context is not None:
			tempClassifier.add_negatives(context)
		
		tempClassifier.train()
		self.categories[class_id] = tempClassifier
		return class_id
	
	def del_category(self,  category_id):
		self.categories.pop(category_id, None)
	
	def increase_samples_category(self, context, sample):
		category_id = self.classify(sample, context)
		self.categories[category_id].increase_sample(context, sample)
	
	def forgetting(self):
		"""
		"""
		for cat in self.categories:
			self.categories[cat].forgetting()
	
	def sample_strength(self, category_id, sample):
		return self.categories[category_id].reaction(sample)
	
	def display_memory(self):
		"""Display function for tests.
		"""
		print 'display ml'
		for cat in self.categories:
			print 'category', cat
			print self.categories[cat].positives
			print self.categories[cat].negatives
		print 'end of display ml'
	
	def display_time(self):
		"""Display function for tests.
		"""
		print 'display_time'
		for cat in self.categories:
			print 'category', cat
			print self.categories[cat].time_positives
			print self.categories[cat].time_negatives
		print 'end of display_time'
	
	def classify(self, elem, context=None):
		"""Returns id of the class that elem is instance of. 
		"""
		abstract()

class MultiRealClassifier(MultiClassifier):
	"""A multi real classifier.
	"""
	def classify(self, elem, context=None):
		"""Returns id of the class that elem is instance of. 
		"""
		if len(self.categories) == 0:
			return None
		
		return max(self.categories.iteritems(), key = 
		           lambda kr: kr[1].reaction(elem)*kr[1].get_weight_sum())[0]

class MultiBinaryClassifier(MultiClassifier):
	"""A multi binary classifier. NOT SUPPORTED IN THIS EXPERIMENT.
	"""
	def classify(self, elem, context):
		"""Returns id of the class that elem is instance of. 
		"""
		if len(self.categories) == 0:
			return None
		#algorithm for finding class that gives the biggest contrast between sample and context
		return max(self.categories.iteritems(), key = 
		           lambda kr: kr[1].reaction(elem)* 
		           (len(context) - sum(map(kr[1].reaction, context))) )[0]
	

def convert_to_classifier(classifier):
	"""Converts a string to a classifier of this name. A conversion should be added here for a new classifier.
	"""
	print 'in convert_to_classifier ', classifier
	if classifier == 'SvmRealClassifier':
		return MultiRealClassifier, smpl.SimpleSvmRealClassifier
	if classifier == 'KnnBinaryClassifier':
		return dircl.DirectClassifier, smpl.SimpleKnnIntClassifier#multi.MultiBinaryClassifier, SingleKnnBinaryClassifier
	if classifier == 'FdaRealClassifier':
		return MultiRealClassifier, smpl.SimpleFdaRealClassifier
