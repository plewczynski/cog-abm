
from math import sqrt

def calc_basic_rates_binary(classifier, positive_class, samples):
	sc = [(s, s.get_class()) for s in samples]
	positive = [s for s,c in sc if c == positive_class]
	negative = [s for s,c in sc if c != positive_class]
	# assertion: len(negative) = tn + fp
	# assertion: len(positive) = tp + fn
	tp = [classifier.classify(s) for s in positive].count(positive_class)
	fp = [classifier.classify(s) for s in negative].count(positive_class)
	tn = len(negative) - fp
	fn = len(positive) - tp

	return (tp, tn, fp, fn)



def calc_basic_rates(classifier, samples):
	tp, tn, fp, fn = 0., 0., 0., 0.
	classes = set([s.get_class() for s in samples])
	for c in classes:
		ttp, ttn, tfp, tfn = calc_basic_rates_binary(classifier, c, samples)
		tp, tn, fp, fn = tp+ttp, tn+ttn, fp+tfp, fn+tfn
	n = len(classes)
	# not shure if this is correct...
	return (tp/n, tn/n, fp/n, fn/n)
		

# from http://en.wikipedia.org/wiki/Receiver_operating_characteristic
# passing basic_rates for speed up
def TPR(classifier, samples, basic_rates = None):
	if basic_rates is None:
		basic_rates = calc_basic_rates(classifier, samples)
	tp, _, _, fn = basic_rates
	return tp / (tp + fn)

def sensitivity(classifier, samples, basic_rates = None):
	return TPR(classifier, samples, basic_rates)

def recall(classifier, samples, basic_rates = None):
	return TPR(classifier, samples, basic_rates)


def FPR(classifier, samples, basic_rates = None):
	if basic_rates is None:
		basic_rates = calc_basic_rates(classifier, samples)
	_, tn, fp, _ = basic_rates
	return fp / (fp + tn)
	

def accuracy(classifier, samples, basic_rates = None):
	if basic_rates is None:
		basic_rates = calc_basic_rates(classifier, samples)
	tp, tn, fp, fn = basic_rates
	return (tp+tn)/(tp+tn+fp+fn)


def TNR(classifier, samples, basic_rates = None):
	return 1. - FPR(classifier, samples, basic_rates)

def specificity(classifier, samples, basic_rates = None):
	return TNR(classifier, samples, basic_rates)


def PPV(classifier, samples, basic_rates = None):
	if basic_rates is None:
		basic_rates = calc_basic_rates(classifier, samples)
	tp, _, fp, _ = basic_rates
	return tp/(tp+fp)
	
def precision(classifier, samples, basic_rates = None):
	return PPV(classifier, samples, basic_rates)


def NPV(classifier, samples, basic_rates = None):
	if basic_rates is None:
		basic_rates = calc_basic_rates(classifier, samples)
	_, tn, _, fn = basic_rates
	return tn/(tn+fn)


def FDR(classifier, samples, basic_rates = None):
	if basic_rates is None:
		basic_rates = calc_basic_rates(classifier, samples)
	tp, _, fp, _ = basic_rates
	return fp/(fp+tp)


def MCC(classifier, samples, basic_rates = None):
	if basic_rates is None:
		basic_rates = calc_basic_rates(classifier, samples)
	tp, tn, fp, fn = basic_rates
	return (tp*tn - fp*fn) / \
		sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))


def AUC(classifier, samples, basic_rates = None):
	# Not implemented yet
	return None
