"""
Most useful things connected with ML
"""
import math
from itertools import izip

class Classifier(object):
	
	def classify(self, sample):
		pass
	
	def classify_pval(self, sample):
		"""
		Returns tuple with class and probability of sample belonging to it
		"""
		pass

	def class_probabilities(self, sample):
		"""
		Returns dict with mapping class->probability that sample belongs to it
		"""
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
		"""
		Symbols should be strings!
		For example Orange doesn't support any other format
		"""
		symbols = [str(s) for s in symbols]
		self.symbols = tuple(s for s in symbols)
		self.mapping = dict(izip(self.symbols, xrange(len(self.symbols))))
#		for i, s in enumerate(symbols):
#			self.mapping[s] = i

	def get_symbol(self, idx):
		return self.symbols[idx]
	
	def get_idx(self, symbol):
		return self.mapping[str(symbol)]
	
	def get_value(self, value):
		return self.get_symbol(value)
	
	def set_value(self, value):
		if str(value) in self.symbols:
			return self.get_idx(value)
		elif value in range(len(self.symbols)):
			return value
		else:
			raise LookupError("Couldn't set attribute to: "+str(value))

	def __eq__(self, other):
		return super(NominalAttribute, self).__eq__(other) and \
			set(self.symbols)==set(other.symbols)


class Sample(object):
	
	def __init__(self, values, meta=None, cls=None, cls_meta=None,
						dist_fun=None, last_is_class=False, cls_idx=None):
		self.values = values[:]
		self.meta = meta or [NumericAttribute() for _ in xrange(len(values))]
		
		if last_is_class or cls_idx is not None:
			if last_is_class:
				cls_idx = -1
			self.cls = self.values[cls_idx]
			self.cls_meta = self.meta[cls_idx]
			self.meta = self.meta[:]
			del self.values[cls_idx]
			del self.meta[cls_idx]
		else:
			self.cls = cls
			self.cls_meta = cls_meta
		
		if self.cls is not None and self.cls_meta is not None:
			self.cls = self.cls_meta.set_value(self.cls)
		for i in xrange(len(self.values)):
			self.values[i] = (self.meta[i]).set_value(self.values[i])

		if dist_fun is None and \
				not [x for x in self.meta if x.ID != NumericAttribute.ID]:
			self.dist_fun = euclidean_distance
		else:
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
	
	def __hash__(self):
		return 3*hash(tuple(self.values)) + 5*hash(self.cls)
	
	def __str__(self):
		return "({0}, {1})".format(str(self.get_values()), self.get_cls())
	
	def __repr__(self):
		return str(self)
	
	def copy_basic(self):
		return Sample(self.values, self.meta, dist_fun=self.dist_fun)
	
	def copy_full(self):
		return Sample(self.values, self.meta, self.cls, self.cls_meta,
																self.dist_fun)

	def copy_set_cls(self, cls, meta):
		s = self.copy_basic()
		s.cls_meta = meta
		s.cls = meta.set_value(cls)
		return s

#Sample distance functions

def euclidean_distance(sx, sy):
	return math.sqrt(math.fsum([
		(x-y)*(x-y) for x, y in izip(sx.get_values(), sy.get_values())
		]))


from scipy.io.arff import loadarff

def load_samples_arff(file_name, last_is_class=False, look_for_cls=True):
	a_data, a_meta = loadarff(file_name)
	names = a_meta.names()
	
	attr = {"nominal":lambda attrs:NominalAttribute(attrs),
			"numeric":lambda _:NumericAttribute()}
	
	gen = (a_meta[n] for n in names)
	meta = [attr[a[0]](a[1]) for a in gen]
	cls_idx = None
	if look_for_cls:
		for i, name in enumerate(names):
			if a_meta[name][0] == "nominal" and name.lower() == "class":
				cls_idx = i
				break

	fun = lambda s: Sample([mi.set_value(vi) for mi, vi in izip(meta, s)],
						meta, last_is_class=last_is_class, cls_idx=cls_idx)

	return [fun(s) for s in a_data]


def split_data(data, train_ratio = 2./3.):
	""" data - samples to split into two sets: train and test
	train_ratio - real number in [0,1]
	
	returns (train, test) - pair of data sets
	"""
	from random import shuffle
	tmp = [s for s in data]
	shuffle(tmp)
	train = [s for i,s in enumerate(tmp) if i<train_ratio*len(tmp)]
	test = [s for i,s in enumerate(tmp) if i>=train_ratio*len(tmp)]
	return (train, test)

