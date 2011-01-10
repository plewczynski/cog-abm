"""
MachineLearningEngine class.
"""
#import PyML
class MachineLearningEngine(object):
	"""
	MachineLearningEngine class.
	
	MachineLearningEngine is high-level classifier that encapsulates typical
	machine learning method from PyML library. 
	
	@sort: __init__, classify, clone, train
	"""
	
	def __init__(self, arg):
		"""
		Initialize MachineLearningEngine.
		
		@attention: When redefining this method to use different machine 
		learning method make sure new low-level classifier implements classify
		method.
		
		@type arg: number
		@param arg: Specifies type of machine learning method.
		"""
		self._train_data_history = []
		if (arg == 1):
			pass
			#TODO_MachineLearning self.classifier= object from PyML
	
	def classify(self, stimulus):
		"""
		Return ID of class, that categorizes stimulus.
		
		@type stimuli: PerceptedStimulus
		@param stimuli: Percepted stimulus as an object of classification.
		
		@rtype: number
		@return: ID of class for stimulus.
		"""
		#return self.classifier.classify(stimulus)
		pass
	
	def clone(self):
		"""
		Return new instance of low-level classifier used by 
		MachineLearningEngine.
		
		@rtype: Classifier
		@return: New instance of classifier.
		"""
		#return self.classifier.deepcopy()
		pass
	
	def train(self, context):
		"""
		TODO_DOC
		"""
		pass
