import math
import sys
import random
sys.path.append("../")
from cog_abm.extras.abstract_meth import *

from itertools import imap, izip, izip_longest
argmax = lambda funct, items: max(izip(imap(funct, items), items))
argmin = lambda funct, items: min(izip(imap(funct, items), items))

def_value = lambda v, default: v and v or default

#Giving the wrapped classifier methods for management of datapoints

class DataPointsCollector(object):
	"""Collects positives and manages them according to time.
	"""
	def_alpha = 0.1
	
	def __init__(self, alpha = None):
		""" @param alpha: forgetting parameter
			 positives: positive samples
			 time_positives: time parameters for positive samples
		"""
		self.alpha = def_value(alpha, DataPointsCollector.def_alpha)
		self.positives = []
		self.time_positives = []
	
	def add_positives(self, new_pos):
		"""Adds positive learning samples to the memory
		"""
		self.positives = self.positives + new_pos
		ones = [1] * len(new_pos)
		self.time_positives = self.time_positives + ones
	
	def increase_sample(self, context, sample):
		""" Adds samples to the memory and retrains the classifier
		"""
		self.add_positives([sample])
	
	def sub_forgetting(self, times, points, threshold):
		""" Forgetting of one list of values.
		"""
		#print 'sub_forgetting start: times: ', times, 'points: ', points
		temp_times = map(self._single_forgetting, times)
		#delete items that are too old
		p_zipped = zip(temp_times, points)
		p_zipped = filter(lambda (time, point): time > threshold,  p_zipped)
		#print 'sub_forgetting: usunieto: times: ', times, 'p_zipped ', p_zipped#len(times) - len(p_zipped)
		if len(p_zipped) == 0:
			temp_times = []
			temp_points = []
		else:
			temp_times, temp_points = zip(*p_zipped)
		return list(temp_times), list(temp_points)
		
	def forgetting(self, threshold = 0.1**30):
		""" Perform forgetting of the samples in the memory.
		"""
		self.time_positives, self.positives = self.sub_forgetting(self.time_positives, self.positives, threshold)
		
	def _single_forgetting(self, a):
		""" A single step of oldening the samples
		"""
		return a*self.alpha

class SingleClassifier(DataPointsCollector):
	"""A base class for a single classifier, wrapping the SimpleClassifier and adding time management.
	"""
	def __init__(self, simple_classifier, alpha=None):
		""" @param simple_classifier: a class inheritating from SimpleClassifier
		""" 
		DataPointsCollector.__init__(self, alpha)
		self.classif_type = simple_classifier
		self.classif = self.classif_type()
		self.negatives = []
		self.time_negatives = []
	
	def train(self):
		"""Retrains the classifier using the memory.
		"""
		temp_cl = self.classif_type()
		arr = self.positives+self.negatives
		etiq = [1] * len(self.positives) + [-1] * len(self.negatives)
		temp_cl.train(arr, etiq)
		self.classif = temp_cl
	
	def add_negatives(self, new_neg):
		"""Adds negative learning samples to the memory
		"""
		self.negatives = self.negatives + new_neg
		ones = [1] * len(new_neg)
		self.time_negatives = self.time_negatives + ones
	
	def increase_sample(self, context, sample):
		""" Adds samples to the memory and retrains the classifier
		"""
		self.add_positives([sample])
		if context <> None:
			self.add_negatives(context)
		self.train()
		
	def forgetting(self, threshold = 0.1**30):
		""" Perform forgetting of the samples in the memory.
		"""
		self.time_positives, self.positives = self.sub_forgetting(self.time_positives, self.positives, threshold)
		self.time_negatives, self.negatives = self.sub_forgetting(self.time_negatives, self.negatives, threshold)
	
	def reaction(self, data):
		"""Returns the reaction of this single classifer for the data.
		"""
		return self.classif.reaction(data)
	def get_weight_sum(self):
		"""Returns the sum of time values for samples.
		"""
		return sum(self.time_positives)
		
		
