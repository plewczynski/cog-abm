#classes of these instances are encapsulated by MultiClassifier and explicitly called here:
from single_classif import *

class MultiClassifier(object):
	"""Base abstract class for all classifiers that use many single classifiers.
	"""
	def __init__(self, simple_classifier_type):
		"""
		@param simple_classifier_type: classifier wrapper used in this specific multi classifier. Has to inherit from SimpleClassifier.
		"""
		self.categories = {}
		self.new_category_id = 0
		self.classif = simple_classifier_type
		#denotes the ability of a classifier to classify:
		self.can_classif = False

	def get_positives(self, class_id):
		"""Returns positives from all the classes except for classifier of class_id id. 
		Needed for negatives for a new class.
		"""
		positives = []
		for cat in self.categories:
			if cat <> class_id:
				positives = positives + self.categories[cat].positives.points
		return positives

	def add_nega_to_all(self, nega, class_id):
		"""Add negatives to all classes except for classifier of class_id id.
		"""
		for cat in self.categories:
			#print "self.categories[cat].negatives ", self.categories[cat].negatives.points, "nega", nega
			if len(self.categories[cat].positives.points) > 0 and class_id <> cat:
				self.categories[cat].add_negatives(nega)
				self.categories[cat].train()

	def add_category(self, sample, class_id = None):
		"""Adds a new category to the categories. Called in discrimination game.
		"""
		#print "In MultiClassif:add_category()."
		if class_id is None:
			#print "New class_id: ",class_id 
			class_id = self.new_category_id
			self.new_category_id += 1
			tempClassifier = SingleClassifier(self.classif)
		else:
			#print "Old class_id: ",class_id
			tempClassifier = self.categories[class_id]
		
		if sample is not None:
			#print "Adding positive: ",sample
			tempClassifier.add_positives([sample])
		
		#add negatives from other samples and this sample to other negatives:
		#add this positive to other classes except the class_id one:
		self.add_nega_to_all([sample], class_id)
		negatives = self.get_positives(class_id)
		if (len(negatives) > 0):
			#print "found negatives to add: ", negatives, "can_classify"
			self.can_classif = True
			#add negatives:
			tempClassifier.add_negatives(negatives)
			#update the classifiers, including the new one:
			tempClassifier.train()
		else:
			#print "No negatives to add."
			self.can_classif = False
		self.categories[class_id] = tempClassifier
		return class_id
	
	def del_category(self,  category_id):
		self.categories.pop(category_id, None)
	
	def increase_samples_category(self, sample):
		category_id = self.classify(sample)
		self.categories[category_id].increase_sample(sample)
		#Add as a negative to others:
		self.add_nega_to_all([sample], category_id)
	
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
			print 'positives: ', self.categories[cat].positives.points
			print 'negatives: ', self.categories[cat].negatives.points
		print 'end of display ml'
	
	def display_time(self):
		"""Display function for tests.
		"""
		print 'display_time'
		for cat in self.categories:
			print 'category', cat
			print 'positives: ', self.categories[cat].positives.time_points
			print 'negatives: ', self.categories[cat].negatives.time_points
		print 'end of display_time'

	def classify(self, elem):
		"""Returns id of the class that elem is instance of. 
		"""
		if self.can_classif == False:
			#print "classify: can't classif"
			return 0
		
		return max(self.categories.iteritems(), key = 
		           lambda kr: kr[1].reaction(elem)*kr[1].get_weight_sum())[0]


