import direct_classif as dircl#needed in convertion method - direct ML methods
import multi_classif as multi#needed in convertion method - multi ML methods
#Concrete ML instances:
import simple_classif_mlpy as smpl#needed in convertion method - MLPY

def convert_to_classifier(classifier):
	"""Converts a string to a classifier of this name. A conversion should be added here for a new classifier.
	"""
	#print 'in convert_to_classifier ', classifier
	if classifier == 'SvmRealClassifier':
		return multi.MultiClassifier, smpl.SimpleSvmRealClassifier
	if classifier == 'KnnIntegerClassifier':
		return dircl.DirectClassifier, smpl.SimpleKnnIntClassifier#multi.MultiBinaryClassifier, SingleKnnBinaryClassifier
	if classifier == 'FdaRealClassifier':
		return multi.MultiClassifier, smpl.SimpleFdaRealClassifier
