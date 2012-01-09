import sys
sys.path.append('../')
import unittest
from cog_abm.ML.orange_wrapper import OrangeClassifier
from cog_abm.ML.core import NominalAttribute, NumericAttribute, Sample
import orange
from itertools import izip


class TestOrange(unittest.TestCase):
    
    
    def setUp(self):
        self.classifiers = [("BayesLearner",[],{}), 
                            ("TreeLearner",[],{}),
                            ("kNNLearner",[],{"k": 1}),
                            ("kNNLearner",[],{"k": 3}),
                            ("TreeLearner",[],{})
                            ]
        self.knn1 = OrangeClassifier(self.classifiers[2][0])
        self.knn3 = OrangeClassifier(self.classifiers[3][0])
        self.tree = OrangeClassifier(self.classifiers[4][0])
    
    
    def test_classifier_creation(self):
        """ Proper classifier creation """

        for (c, args, kargs) in self.classifiers:
            classifier = OrangeClassifier(c, *args, **kargs)
            self.assertEqual(getattr(orange, c),
                             type(classifier.classifier))
        
    
    def test_classification(self):
        cls_meta = NominalAttribute([0,1])
        meta = [NumericAttribute() for _ in xrange(3)]
        train_set = [Sample([0, 0, 0], meta, 0, cls_meta),
                     Sample([0, 1, 0], meta, 0, cls_meta),
                     Sample([0, 0, 1], meta, 0, cls_meta),
                     Sample([3, 0, 0], meta, 1, cls_meta),
                     Sample([3, 1, 0], meta, 1, cls_meta),
                     Sample([3, 0, 1], meta, 1, cls_meta),
                     ]

        classifier = self.knn1
#        classifier = self.tree
        classifier.train(train_set)
        expected = [str(x) for x in [ 0, 0, 0, 1, 1, 1, 0, 1]]
        samples = [s for s in train_set]
        samples.extend([Sample([1, 0, 0], meta), Sample([2, 1, 0], meta)])
        for e, s in izip(expected, samples):
            self.assertEqual(e, classifier.classify(s))
            k, p = classifier.classify_pval(s)
            self.assertTrue(0.<= p <= 1.)
            self.assertEqual(k, classifier.classify(s))
            p2 = classifier.class_probabilities(s)
            self.assertAlmostEqual(1., sum(p2.values()), delta=0.00001)

