"""
Most useful things connected with ML
"""
from itertools import izip
from cog_abm.extras.tools import def_value
import math


class Classifier(object):
	
	def classify(self, sample):
		pass
	

	def train(self, samples):
		pass

	
	def clone(self):
		"""
		Returns copy of classifier. This is default implementation.
		Should be overriden in subclasses.
		
		@rtype: Classifier
		@return: New instance of classifier.
		"""
		import copy
		return copy.deepcopy(self)




class Attribute(object):
	
	ID = None
	""" This class field is for id when putting some conversion method in dict
	"""
	
	def get_value(self, value):
		pass
	
	
	def set_value(self, value):
		return value
	
	
	def __eq__(self, other):
		return self.ID==other.ID



class NumericAttribute(Attribute):
	
	ID = "NumericAttribute"
	
	def get_value(self, value):
		return value


	
class NominalAttribute(Attribute):
	
	ID = "NominalAttribute"
	
	def __init__(self, symbols):
		self.symbols = tuple(s for s in symbols)
		self.mapping = dict(izip(self.symbols, xrange(len(self.symbols))))
#		for i, s in enumerate(symbols):
#			self.mapping[s] = i


	def get_symbol(self, idx):
		return self.symbols[idx]
	

	def get_idx(self, symbol):
		return self.mapping[symbol]
	

	def get_value(self, value):
		return self.get_symbol(value)
	
	
	def set_value(self, value):
		if value in self.symbols:
			return self.get_idx(value)
		elif value in range(len(self.symbols)):
			return value
		else:
			raise LookupError

		
	def __eq__(self, other):
		return super(NominalAttribute, self).__eq__(other) and \
			self.symbols==other.symbols



class Sample(object):
	
	
	def __init__(self, values, meta = None, cls = None, cls_meta = None,
								 dist_fun = None, last_is_class = False):
		self.values = values
		self.meta = def_value(meta,
						[NumericAttribute() for _ in xrange(len(values))])
		
		if last_is_class:
			self.cls = self.values[-1]
			self.cls_meta = self.meta[-1]
			self.values = self.values[:-1]
			self.meta = self.meta[:-1]
		else:
			self.cls = cls
			self.cls_meta = cls_meta
			
		self.dist_fun = dist_fun
	
	
	def get_cls(self):
		if self.cls_meta is None or self.cls is None:
			return None
		
		return self.cls_meta.get_value(self.cls)


	def get_values(self):
		return [m.get_value(v) for v, m in izip(self.values, self.meta)]


	def distance(self, other):
		return self.dist_fun(self, other)
	
	
	def __eq__(self, other):
		return self.cls==other.cls and self.cls_meta==other.cls_meta and \
			self.meta==other.meta and self.values==other.values
		
	
	def __str__(self):
		return "({0}, {1})".format(str(self.get_values()), self.cls)

#Sample distance functions

def euclidean_distance(sx, sy):
	return math.sqrt(math.fsum([
		(x-y)**2. for x, y in izip(sx.get_values(), sy.get_values())
		]))



from scipy.io.arff import loadarff

def load_samples_arff(file_name):
	a_data, a_meta = loadarff(file_name)
	names = a_meta.names()
			
	attr = {"nominal":lambda attrs:NominalAttribute(attrs),
			"numeric":lambda _:NumericAttribute()}
	
	gen = (a_meta[n] for n in names)
	meta = [attr[a[0]](a[1]) for a in gen]
	last_is_class = \
		names[-1].lower() == "class" and a_meta[names[-1]][0] == "nominal"
	
	fun = lambda s: Sample([mi.set_value(vi) for mi, vi in izip(meta, s)],
						meta, last_is_class = last_is_class)

	return [fun(s) for s in a_data]


def split_data(data, train_ratio = 2./3.):
	""" data - samples to split into two sets: train and test
	train_ratio - real number in [0,1]
	
	returns (train, test) - pair of data sets
	"""
	from random import shuffle
	tmp = [s for s in data]
	shuffle(tmp)
	train = [s for i,s in enumerate(data) if i<train_ratio*len(data)]
	test = [s for i,s in enumerate(data) if i>=train_ratio*len(data)]
	return (train, test)

