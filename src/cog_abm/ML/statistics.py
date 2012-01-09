import math


def calc_basic_rates(classifier, samples, positive_class):
	positive_class = str(positive_class)
	sc = [(s, s.get_cls()) for s in samples]
	positive = [s for s,c in sc if c == positive_class]
	negative = [s for s,c in sc if c != positive_class]
	tp = [classifier.classify(s) for s in positive].count(positive_class)
	fp = [classifier.classify(s) for s in negative].count(positive_class)
	tn = len(negative) - fp
	fn = len(positive) - tp
	return tuple( float(x) for x in (tp, tn, fp, fn))


def basic_rates_based(fn):
	def calculator(classifier, samples, positive_class, basic_rates = None):
		if basic_rates is None:
			basic_rates = calc_basic_rates(classifier, samples, positive_class)
		try:
			return fn(classifier, samples, positive_class, basic_rates)
		except ZeroDivisionError:
			return 0.
	return calculator


# from http://en.wikipedia.org/wiki/Receiver_operating_characteristic
# passing basic_rates for speed up

@basic_rates_based
def TPR(classifier, samples, positive_class, basic_rates = None):
	tp, _, _, fn = basic_rates
	return tp / (tp + fn)

def sensitivity(classifier, samples, positive_class, basic_rates = None):
	return TPR(classifier, samples, positive_class, basic_rates)

def recall(classifier, samples, positive_class, basic_rates = None):
	return TPR(classifier, samples, positive_class, basic_rates)

@basic_rates_based
def FPR(classifier, samples, positive_class, basic_rates = None):
	_, tn, fp, _ = basic_rates
	return fp / (fp + tn)


@basic_rates_based
def accuracy(classifier, samples, positive_class, basic_rates = None):
	tp, tn, fp, fn = basic_rates
	return (tp+tn)/(tp+tn+fp+fn)


def TNR(classifier, samples, positive_class, basic_rates = None):
	return 1. - FPR(classifier, samples, positive_class, basic_rates)

def specificity(classifier, samples, positive_class, basic_rates = None):
	return TNR(classifier, samples, positive_class, basic_rates)


@basic_rates_based
def PPV(classifier, samples, positive_class, basic_rates = None):
	tp, _, fp, _ = basic_rates
	return tp/(tp+fp)
	
def precision(classifier, samples, positive_class, basic_rates = None):
	return PPV(classifier, samples, positive_class, basic_rates)


@basic_rates_based
def NPV(classifier, samples, positive_class, basic_rates = None):
	_, tn, _, fn = basic_rates
	return tn/(tn+fn)


@basic_rates_based
def FDR(classifier, samples, positive_class, basic_rates = None):
	tp, _, fp, _ = basic_rates
	return fp/(fp+tp)


@basic_rates_based
def MCC(classifier, samples, positive_class, basic_rates = None):
	tp, tn, fp, fn = basic_rates
	return (tp*tn - fp*fn) / \
		math.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))


@basic_rates_based
def AUC(classifier, samples, positive_class, basic_rates = None):
	# Not implemented yet
	return None


def correct(classifier, samples):
	return math.fsum([int(classifier.classify(s)==s.get_cls())
											 for s in samples])/len(samples)

