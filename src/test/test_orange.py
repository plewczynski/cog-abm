import sys
from cog_abm.stimuli.perception import VectorPerception
sys.path.append('../')
import unittest
from cog_abm.ML.orange_wrapper import OrangeClassifier
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
        train_set = [([0, 0, 0], 0), ([0, 1, 0], 0), ([0, 0, 1], 0),
                     ([3, 0, 0], 1), ([3, 1, 0], 1), ([3, 0, 1], 1),
                     ]
        classifier = self.knn1
#        classifier = self.tree
        classifier.train(train_set)
        expected = [ 0, 0, 0, 1, 1, 1, 0, 1]
        stimuli = [e[0] for e in train_set]
        stimuli.extend([[1, 0, 0], [2,1,0]])
        for e, s in izip(expected, stimuli):
            self.assertEqual(e, classifier.classify(s))
        
        
#    def test_to_help(self):
#        
#        
#        