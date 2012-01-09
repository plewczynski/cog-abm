import sys
sys.path.append('../')
import unittest
from cog_abm.ML.core import *
from cog_abm.extras.additional_tools import StupidClassifer
from cog_abm.ML.statistics import *


class TestStatistics(unittest.TestCase):
    
    def setUp(self):
        self.meta = [NumericAttribute(), NominalAttribute([0, 1])]
        self.samples = [Sample([i, 0], self.meta, last_is_class=True) 
                        for i in xrange(10)] + \
                        [Sample([i, 1], self.meta, last_is_class=True)
                         for i in xrange(10,15)]
        
        self.classifiers = tuple(StupidClassifer(i) for i in xrange(2))
        self.basics = tuple([(10., 0., 5., 0.), (0., 5., 0., 10.)])



    def gen(self, f):
        return [f(self.classifiers[i], self.samples, 0) for i in [0,1]]
    
    
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
        self.do_tst([2./3., 1./3.], accuracy)
        

    def test_TNR(self):
        self.do_tst([0., 1.], TNR)
        

    def test_specificity(self):
        self.do_tst([0., 1.], specificity)
        

    def test_PPV(self):# error
        self.do_tst([2./3., 0.], PPV)
        

    def test_precision(self):
        self.do_tst([2./3., 0.], precision)
        

    def test_NPV(self):
        self.do_tst([0., 1./3.], NPV)
        

    def test_FDR(self):
        self.do_tst([1./3., 0.], FDR)
        

    def test_MCC(self):
        self.do_tst([0., 0.], MCC)
    
    def test_correct(self):
        self.do_tst([2./3, 1./3.], lambda cl, s, _: correct(cl,s))
        
    @unittest.skip("Not implemented yet!")
    def test_AUC(self):
        self.do_test(["NOT IMPLEMENTED"], AUC)
        

