import math

from collections import namedtuple
from itertools import combinations, groupby

from cog_abm.extras.tools import avg, calc_std, calc_auc


def calc_basic_rates(classifier, samples, positive_class):
    positive_class = str(positive_class)
    sc = [(s, s.get_cls()) for s in samples]
    positive = set(s for s, c in sc if c == positive_class)
    negative = set(s for s, c in sc if c != positive_class)
    tp = [classifier.classify(s) for s in positive].count(positive_class)
    fp = [classifier.classify(s) for s in negative].count(positive_class)
    tn = len(negative) - fp
    fn = len(positive) - tp
    return tuple(float(x) for x in (tp, tn, fp, fn))


def basic_rates_based(fn):
    def calculator(classifier, samples, positive_class, basic_rates=None):
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
def TPR(classifier, samples, positive_class, basic_rates=None):
    tp, _, _, fn = basic_rates
    return tp / (tp + fn)


def sensitivity(classifier, samples, positive_class, basic_rates=None):
    return TPR(classifier, samples, positive_class, basic_rates)


def recall(classifier, samples, positive_class, basic_rates=None):
    return TPR(classifier, samples, positive_class, basic_rates)


@basic_rates_based
def FPR(classifier, samples, positive_class, basic_rates=None):
    _, tn, fp, _ = basic_rates
    return fp / (fp + tn)


@basic_rates_based
def accuracy(classifier, samples, positive_class, basic_rates=None):
    tp, tn, fp, fn = basic_rates
    return (tp + tn) / (tp + tn + fp + fn)


def TNR(classifier, samples, positive_class, basic_rates=None):
    return 1. - FPR(classifier, samples, positive_class, basic_rates)


def specificity(classifier, samples, positive_class, basic_rates=None):
    return TNR(classifier, samples, positive_class, basic_rates)


@basic_rates_based
def PPV(classifier, samples, positive_class, basic_rates=None):
    tp, _, fp, _ = basic_rates
    return tp / (tp + fp)


def precision(classifier, samples, positive_class, basic_rates=None):
    return PPV(classifier, samples, positive_class, basic_rates)


@basic_rates_based
def NPV(classifier, samples, positive_class, basic_rates=None):
    _, tn, _, fn = basic_rates
    return tn / (tn + fn)


@basic_rates_based
def FDR(classifier, samples, positive_class, basic_rates=None):
    tp, _, fp, _ = basic_rates
    return fp / (fp + tp)


@basic_rates_based
def MCC(classifier, samples, positive_class, basic_rates=None):
    tp, tn, fp, fn = basic_rates
    return (tp * tn - fp * fn) / \
            math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))


def correct(classifier, samples):
    return math.fsum([int(classifier.classify(s) == s.get_cls())
                            for s in samples]) / len(samples)


ClassifiedSample = namedtuple("ClassifiedSample", "sample cls distribution")


def classify_samples(classifier, samples):
    def tmp(sample):
        d = classifier.class_probabilities(sample)
        cls = classifier.classify(sample)
        return ClassifiedSample(sample, cls, d)
    return map(tmp, samples)


def group_by_classes(samples, key=lambda s: s.get_cls()):
    ''' This function groups samples into sets containing the same class
    IMPORTANT:
        **This will skip empty classes (it takes them from samples)**
    '''
    s = sorted(samples, key=key)
    return dict(((cls, list(l)) for cls, l in groupby(s, key=key)))


def ROC(classifier, samples, positive_class):
    return _ROC(classify_samples(classifier, samples), positive_class)


def _ROC(classified_test_samples, positive_class):
    key = lambda classified_sample: \
                        classified_sample.distribution.get(positive_class, 0.)
    L = sorted(classified_test_samples, key=key, reverse=True)
    res = []
    fp, tp = 0., 0.
    prev_prob = -1  # this guarantee that (0, 0) will be in resulting list
    for sample, classifier_class, distrib in L:
        prob = distrib.get(positive_class, 0.)
        if prob != prev_prob:
            res.append((fp, tp))
        prev_prob = prob
        if sample.get_cls() == positive_class:
            tp += 1
        else:
            fp += 1
    res.append((fp, tp))
    if tp == 0:
        tp = 1
        # this is dirty hack - there were no positive samples in data
        # so eighter way we will get there 0
    if fp == 0:
        fp = 1

    return [(x / fp, y / tp) for x, y in res]


def AUCROC_weighting(gbc):
    N = math.fsum([len(samples) for _, samples in gbc.iteritems()])
    N2 = N * N
    waucs = [(len(samples1) * len(samples2) / N2, calc_auc(_ROC(samples1 + samples2, cls1)))
        for (cls1, samples1), (cls2, samples2) in combinations(gbc.items(), 2)]
    wsum = math.fsum((x[0] for x in waucs))
    # TODO can wsum be 0? what if?
    return math.fsum(map(lambda x: x[0] * x[1], waucs)) / wsum


def AUCROC_nonweighting(gbc):
    return avg([calc_auc(_ROC(samples1 + samples2, cls1))
        for (cls1, samples1), (cls2, samples2) in combinations(gbc.items(), 2)])


def AUCROC(classifier, test_samples, weighted=False):
    ''' Weighted version seems to be more common...
     but is computationally more expensive
    '''
    classified_samples = classify_samples(classifier, test_samples)
    if filter(lambda cs: cs.cls is None, classified_samples):
        return 0.
    gbc = group_by_classes(classified_samples, key=lambda cs: cs.sample.get_cls())
    if weighted:
        f = AUCROC_weighting
    else:
        f = AUCROC_nonweighting
    return f(gbc)


def classifier_single_performance(classifier, train, test, measure):
    ''' Trains and evaluates classifier on given test sets
    '''
    classifier.train(train)
    return measure(classifier, test)


def avg_classifier_performance(classifier, data_sets, measure):
    ''' Returns average and std dev of classifier performance over
    train and test sets using given measure
    '''
    return calc_std([classifier_single_performance(classifier,
        train, test, measure) for train, test in data_sets])


def aucroc_avg_classifier_performance(classifier, data_sets):
    ''' This is defined just because this might be used quite often
    '''
    return avg_classifier_performance(classifier, data_sets, AUCROC)
