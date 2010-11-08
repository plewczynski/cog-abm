import math
import sys
import random
import numpy as np
import mlpy
sys.path.append("../")

from itertools import imap, izip, izip_longest
argmax = lambda funct, items: max(izip(imap(funct, items), items))
argmin = lambda funct, items: min(izip(imap(funct, items), items))

def_value = lambda v, defult: v and v or defult
import numpy as np
import mlpy


class SingleFdaRealClassifier(object):
	""" Adaptive network is some kind of classifier
	"""
	
	def __init__(self, k=1):
		"""
		"""
		self.classifier = mlpy.Fda(k) # initialize Fda class
		self.positives = []
		self.negatives = []
		self.time_positives = []
		self.time_negatives = []
		self.num_neigh = k
	
	def train_fda(self):
		"""
		"""
		fda = mlpy.Fda(self.num_neigh)
		arr = np.array(self.positives+self.negatives)
		etiq = np.array([1] * len(self.positives) + [-1] * len(self.negatives))
		fda.compute(arr, etiq)
		self.classifier = fda
	
	
	def add_positives(self, new_pos):
		"""
		"""
		self.positives = self.positives + new_pos
		ones = [1] * len(new_pos)
		self.time_positives = self.time_positives + ones
		
		
	def add_negatives(self, new_neg):
		"""
		"""
		self.negatives = self.negatives + new_neg
		min_ones = [-1] * len(new_neg)
		ones = [1] * len(new_neg)
		self.time_negatives = self.time_negatives + ones
		
		
	def reaction(self,  data):
		"""
		"""
		xtr = np.array(data)
		self.classifier.predict(xtr)
		return self.classifier.realpred
	
	
	def increase_sample(self, context, sample):
		""" 
		"""
		self.add_positives([sample])
		if context <> None:
			self.add_negatives(context)
		self.train_fda
	
	
	
	def forgetting(self, threshold = 5):
		self.time_positives = map(self._single_forgetting, self.time_positives)
		self.time_negatives = map(self._single_forgetting, self.time_negatives)
		#delete items that are too old
		posi_zipped = zip(self.time_positives, self.positives)
		posi_zipped = filter(lambda (time, point): time < threshold,  posi_zipped)
		if len(posi_zipped) == 0:
			self.time_positives = []
			self.positives = []
		else:
			time_posi, posi = zip(*posi_zipped)
			self.time_positives = list(time_posi)
			self.positives = list(posi)
		
		neg_zipped = zip(self.time_negatives, self.negatives)
		neg_zipped = filter(lambda (time, point): time < threshold,  neg_zipped)
		if len(neg_zipped) == 0:
			self.time_negatives = []
			self.negatives = []
		else:
			time_negs, negs = zip(*neg_zipped)
			self.time_negatives = list(time_negs)
			self.negatives = list(negs)
	
	def _single_forgetting(self, a):
		return a+1
	
	
	
class FdaRealClassifier(object):
	
	def __init__(self):
		self.categories = {}
		self.new_category_id = 0
	
	
	def add_category(self, sample = None, context = None, class_id = None):
		#print 'in add category'
		if class_id is None:
			#print 'new class_id'
			class_id = self.new_category_id
			self.new_category_id += 1
			singleClassifier = SingleFdaRealClassifier()
		
		else:
			singleClassifier = self.categories[class_id]
		
		if sample is not None:
			singleClassifier.add_positives([sample])
		
		if context is not None:
			singleClassifier.add_negatives(context)
		
		singleClassifier.train_fda()
				
		self.categories[class_id] = singleClassifier
		return class_id
		
	
	
	def del_category(self,  category_id):
		self.categories.pop(category_id, None)

	
	def classify(self,  elem):
		if len(self.categories) == 0:
			return None
		
		return max(self.categories.iteritems(), key = 
		           lambda kr: kr[1].reaction(elem))[0]
	
	
	def increase_samples_category(self, context, sample):
		#print 'increase_samples_category', sample
		category_id = self.classify(sample)
		self.categories[category_id].increase_sample(context, sample)
	
	
	def forgetting(self, threshold = 3):
		
		for cat in self.categories:
			self.categories[cat].forgetting()
	
	
	def sample_strength(self, category_id, sample):
		return self.categories[category_id].reaction(sample)
	
	def display_memory(self):
		#print 'display ml'
		for cat in self.categories:
			pass#print 'category', cat
			#print self.categories[cat].positives
			#print self.categories[cat].negatives
		#print 'end of display ml'
	
	def display_time(self):
		#print 'display_time'
		for cat in self.categories:
			pass#print 'category', cat
			#print self.categories[cat].time_positives
			#print self.categories[cat].time_negatives
		#print 'end of display_time'



if __name__ == "__main__":
    #xtr = np.array([[1, 2, 3], [3, 4, 5], # first sample
    # [2, 3, 4], # second sample
    # [0, 1, 4]]) # third sample
    #ytr = np.array([1, -1, -1, -1]) # classes
    #fda = mlpy.fda() # initialize fda class
    ##print fda.compute(xtr, ytr) # compute fda
    #test_point = np.array([1, 2, 3])
    ##print fda.predict(test_point)
        
    
    
    sample = [1, 2, 3]
    a = [2, 3, 4]
    b = [3, 4, 5]
    c = [0, 1, 4]
    d = [2.5, 3.5, 4.5]
    xtr = np.array([sample, a, b, c])
    ytr = np.array([1, -1, -1, -1]) # classes
    fda = mlpy.Fda() # initialize Fda class
    ##print Fda.compute(xtr, ytr) # compute Fda
    #test_point = np.array([1, 2, 3])
    ##print Fda.predict(test_point)
    ##print Fda.realpred
    #test_point = np.array([4, 5, 6])
    ##print Fda.predict(test_point)
    ##print Fda.realpred
    test_point = np.array([10, 11, 23])
    ##print Fda.predict(test_point)
    ##print Fda.realpred
    #test_point = np.array([1, 2.5, 3])
    ##print Fda.predict(test_point)
    ##print Fda.realpred
    
    #test learning:
    #print 'new experiment'
    ml = FdaRealClassifier()
    ml.add_category(sample, [a, b, c])
    print ml.classify(sample)
    print ml.classify(a)
    print ml.classify(b)
    print ml.classify(c)
    ml.add_category(c, [sample, b, a])
    print ml.classify(sample)
    print ml.classify(a)
    print ml.classify(b)
    print ml.classify(c)
    #test forgetting:
    print 'test forgetting'
    ml.display_time()
    ml.forgetting()
    ml.display_time()
    ml.forgetting()
    print ml.classify(d)
    ml.increase_samples_category([sample, b], d)
    ml.display_time()
    print 'a1aaaaaaaaaaaaaaaaaaaaaaa'
    ml.forgetting()
    ml.display_time()
    ml.display_memory()
    print 'a2aaaaaaaaaaaaaaaaaaaaaaa'
    ml.forgetting()
    ml.display_time()
    ml.display_memory()
    print ml.classify(sample)
    print ml.classify(a)
    print ml.classify(b)
    print ml.classify(c)
    