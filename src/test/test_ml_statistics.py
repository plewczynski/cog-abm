import random
import sys
sys.path.append('../')

import unittest
from cog_abm.ML.core import NumericAttribute, NominalAttribute, Sample, split_data_cv
from cog_abm.extras.additional_tools import StupidClassifer
from cog_abm.ML.statistics import calc_basic_rates, TPR, sensitivity, \
    recall, FPR, accuracy, TNR, specificity, PPV, precision, NPV, FDR, \
    MCC, correct, ROC, AUCROC, aucroc_avg_classifier_performance
from cog_abm.ML.orange_wrapper import OrangeClassifier


def simple_meta_attrs(class_attrs=[0, 1]):
    return [NumericAttribute(), NominalAttribute(list(class_attrs))]


class TestBasicStatistics(unittest.TestCase):

    def setUp(self):
        self.meta = simple_meta_attrs()
        self.samples = [Sample([i, 0], self.meta, last_is_class=True)
                        for i in xrange(10)] + \
                        [Sample([i, 1], self.meta, last_is_class=True)
                         for i in xrange(10, 15)]

        self.classifiers = tuple(StupidClassifer(i) for i in xrange(2))
        self.basics = tuple([(10., 0., 5., 0.), (0., 5., 0., 10.)])

    def gen(self, f):
        return [f(self.classifiers[i], self.samples, 0) for i in [0, 1]]

    def do_tst(self, v, f):
        self.assertSequenceEqual(v, self.gen(f))

    def test_basic_rates(self):
        self.do_tst(self.basics, calc_basic_rates)

    def test_TPR(self):
        self.do_tst([1., 0.], TPR)

    def test_sensitivity(self):
        self.do_tst([1., 0.], sensitivity)

    def test_recall(self):
        self.do_tst([1., 0.], recall)

    def test_FPR(self):
        self.do_tst([1., 0.], FPR)

    def test_accuracy(self):
        self.do_tst([2. / 3., 1. / 3.], accuracy)

    def test_TNR(self):
        self.do_tst([0., 1.], TNR)

    def test_specificity(self):
        self.do_tst([0., 1.], specificity)

    def test_PPV(self):  # error
        self.do_tst([2. / 3., 0.], PPV)

    def test_precision(self):
        self.do_tst([2. / 3., 0.], precision)

    def test_NPV(self):
        self.do_tst([0., 1. / 3.], NPV)

    def test_FDR(self):
        self.do_tst([1. / 3., 0.], FDR)

    def test_MCC(self):
        self.do_tst([0., 0.], MCC)

    def test_correct(self):
        self.do_tst([2. / 3, 1. / 3.], lambda cl, s, _: correct(cl, s))


class TestAUCROCStatistics(unittest.TestCase):

    def setUp(self):
        self.meta = simple_meta_attrs(['-', '+'])
        self.cs = lambda i, v: Sample([i, self.meta[1].set_value(v)], self.meta, last_is_class=True)
        self.classifier = OrangeClassifier('kNNLearner', k=1)
        test_samples = '+++-++-+-+--+---'
        N = len(test_samples)
        train_samples = ('+' * (N / 2)) + ('-' * (N / 2))
        self.test_samples, self.train_samples = ([self.cs(i, v) for i, v in enumerate(samples)]
            for samples in [test_samples, train_samples])
        random.shuffle(self.test_samples)
        self.classifier.train(self.train_samples)

    def _test_roc_eq(self):
        roc = ROC(self.classifier, self.test_samples, '+')
        middle = roc[1]
        tpr, fpr = map(lambda f: f(self.classifier, self.test_samples, '+'), [TPR, FPR])
        self.assertEqual(middle[1], tpr)
        self.assertEqual(middle[0], fpr)

    def test_ROC(self):
        self._test_roc_eq()

    def _test_auc_eq(self):
        tpr, fpr = map(lambda f: f(self.classifier, self.test_samples, '+'), [TPR, FPR])
        auc = AUCROC(self.classifier, self.test_samples)
        expected_area = fpr * tpr / 2 + (1 - fpr) * (tpr + 1) / 2
        expected_area_v2 = (1 + tpr - fpr) / 2.
        self.assertEqual(expected_area, expected_area_v2)
        # ^^^ just checking my math :)
        self.assertEqual(auc, expected_area)

    def test_AUC(self):
        self._test_auc_eq()

    def test_multiplerandom_test(self):
        N = len(self.test_samples)

        def gen_test_case():
            schema = ''.join(['+' if random.random() >= 0.5 else '-' for _ in xrange(N)])
            return [self.cs(i, v) for i, v in enumerate(schema)]

        for _ in xrange(200):
            train = gen_test_case()
            self.classifier.train(train)
            self._test_roc_eq()
            self._test_auc_eq()

    def test_avg_auc_roc_with_splited_cv(self):
        sets = split_data_cv(self.test_samples)

        def tmp(train, test):
            self.classifier.train(train)
            return AUCROC(self.classifier, test)
        aucs = [tmp(train, test) for train, test in sets]
        max_auc, min_auc = (f(aucs) for f in (max, min))
        avg_auc = aucroc_avg_classifier_performance(self.classifier, sets)
        self.assertTrue(min_auc <= avg_auc[0] <= max_auc)
