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
	"""Collects points and manages them according to time.
	"""
	def_alpha = 0.1
	
	def __init__(self, alpha = None):
		""" @param alpha: forgetting parameter
			 points: samples
			 time_points: time parameters for samples
		"""
		self.alpha = def_value(alpha, DataPointsCollector.def_alpha)
		self.points = []
		self.time_points = []
	
	def add_points(self, new_poi):
		"""Adds new_poi learning samples to the memory
		"""
		self.points = self.points + new_poi
		ones = [1] * len(new_poi)
		self.time_points = self.time_points + ones
	
	def increase_sample(self, sample):
		""" Adds samples to the memory and retrains the classifier
		"""
		self.add_points([sample])
	
	def sub_forgetting(self, times, points, threshold):
		""" Forgetting of one list of values.
		"""
		temp_times = map(self._single_forgetting, times)
		#delete items that are too old
		p_zipped = zip(temp_times, points)
		p_zipped = filter(lambda (time, point): time > threshold,  p_zipped)
		if len(p_zipped) == 0:
			temp_times = []
			temp_points = []
		else:
			temp_times, temp_points = zip(*p_zipped)
		return list(temp_times), list(temp_points)
		
	def forgetting(self, threshold = 0.1**30):
		""" Perform forgetting of the samples in the memory.
		"""
		self.time_points, self.points = self.sub_forgetting(self.time_points, self.points, threshold)
		
	def _single_forgetting(self, a):
		""" A single step of oldening the samples
		"""
		return a*self.alpha

class SingleClassifier(object):
	"""A base class for a single classifier, wrapping the SimpleClassifier and adding time management.
	"""
	def __init__(self, simple_classifier, alpha=None):
		""" @param simple_classifier: a class inheritating from SimpleClassifier
		""" 
		self.classif_type = simple_classifier
		self.classif = self.classif_type()
		self.negatives = DataPointsCollector(alpha)
		self.positives = DataPointsCollector(alpha)
	
	def train(self):
		"""Retrains the classifier using the memory.
		"""
		temp_cl = self.classif_type()
		arr = self.positives.points+self.negatives.points
		etiq = [1] * len(self.positives.points) + [-1] * len(self.negatives.points)
		temp_cl.train(arr, etiq)
		self.classif = temp_cl
	
	def add_negatives(self, new_neg):
		"""Adds negative learning samples to the memory
		"""
		self.negatives.add_points(new_neg)

	def add_positives(self, new_pos):
		"""Adds positive learning samples to the memory
		"""
		self.positives.add_points(new_pos)
	
	def increase_sample(self, sample):
		""" Adds samples to the memory and retrains the classifier
		"""
		self.add_positives([sample])
		if len(self.negatives.points) > 0:
			self.train()
		
	def forgetting(self, threshold = 0.1**30):
		""" Perform forgetting of the samples in the memory.
		"""
		self.positives.forgetting()
		self.negatives.forgetting()
	
	def reaction(self, data):
		"""Returns the reaction of this single classifer for the data.
		"""
		return self.classif.reaction(data)
	def get_weight_sum(self):
		"""Returns the sum of time values for positive samples.
		"""
		return sum(self.positives.time_points)
		
		
