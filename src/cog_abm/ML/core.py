"""
Most useful things connected with ML
"""
from itertools import izip


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
	
	
	def __init__(self, values, meta, cls = None, cls_meta = None):
		self.values = values
		self.meta = meta
		self.cls = cls
		self.cls_meta = cls_meta
	
	
	def get_cls(self):
		if self.cls_meta is None or self.cls is None:
			return None
		
		return self.cls_meta.get_value(self.cls)


	def get_values(self):
		return [m.get_value(v) for v, m in izip(self.values, self.meta)]

