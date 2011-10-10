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



class Sample(object):
	
	
	def __init__(self, values, meta = None, cls = None, cls_meta = None,
								 dist_fun = None):
		self.values = values
		self.meta = def_value(meta, 
						[NumericAttribute() for _ in xrange(len(values))])
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
		return self.cls == other.cls and self.cls_meta==other.cls_meta and \
			self.meta == other.meta and self.values == other.values



#Sample distance functions

def euclidean_distance(sx, sy):
	return math.sqrt(math.fsum([
		(x-y)**2. for x, y in izip(sx.get_values(), sy.get_values())
		]))


