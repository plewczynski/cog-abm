import sys
sys.path.append('../')
import unittest
from steels.multi_classif import *
from steels.simple_classif import *

class TestMultiClassif(unittest.TestCase):
    def test_real_fda(self):
        #test learning
        sample = [1, 2, 3]
        a = [2, 3, 4]
        b = [3, 4, 5]
        c = [0, 1, 4]
        d = [2.5, 3.5, 4.5]
        ml = MultiRealClassifier(SimpleFdaRealClassifier)
        ml.add_category(sample, [a, b, c])
        self.assertEqual(ml.classify(sample, [a, b, c]), 0)
        self.assertEqual(ml.classify(a, [sample, b, c]), 0)
        self.assertEqual(ml.classify(b, [a, sample, c]), 0)
        self.assertEqual(ml.classify(c, [a, b, sample]), 0)
        ml.add_category(c, [sample, b, a])
        self.assertEqual(ml.classify(sample, [c, b, a]), 0)
        self.assertEqual(ml.classify(a, [sample, b, c]), 0)
        self.assertEqual(ml.classify(b, [sample, a, c]), 1)
        self.assertEqual(ml.classify(c, [sample, b, a]), 1)
        #test forgetting:
        #ml.display_time()
        ml.forgetting()
        #ml.display_time()
        ml.forgetting()
        self.assertEqual(ml.classify(d, [a, b, c]), 0)
        ml.increase_samples_category([sample, b], d)
        #ml.display_time()
        ml.forgetting()
        #ml.display_time()
        #ml.display_memory()
        ml.forgetting()
        #ml.display_time()
        #ml.display_memory()
        self.assertEqual(ml.classify(sample, [a, b, c]), 0)
        self.assertEqual(ml.classify(a, [sample, b, c]), 0)
        self.assertEqual(ml.classify(b, [a, sample, c]), 1)
        self.assertEqual(ml.classify(c, [a, b, sample]), 1)
    def test_real_svm(self):
        #test learning
        sample = [1, 2, 3]
        a = [2, 3, 4]
        b = [3, 4, 5]
        c = [0, 1, 4]
        d = [2.5, 3.5, 4.5]
        ml = MultiRealClassifier(SimpleSvmRealClassifier)
        ml.add_category(sample, [a, b, c])
        ml.add_category(d, [a, b, c])
        self.assertEqual(ml.classify(sample, [a, b, c]), 0)
        self.assertEqual(ml.classify(a, [sample, b, c]), 1)
        self.assertEqual(ml.classify(b, [a, sample, c]), 1)
        self.assertEqual(ml.classify(c, [a, b, sample]), 1)
        ml.add_category(c, [sample, b, a])
        #print ml.classify(sample, [c, b, a])#, 0)
        #print ml.classify(a, [sample, b, c])#, 1)
        #print ml.classify(b, [sample, a, c])#, 0)
        #print ml.classify(c, [sample, b, a])#, 1)
        #test forgetting:
        #ml.display_time()
        #print 'ml.forgetting'
        ml.forgetting()
        #ml.display_time()
        #print 'ml.forgetting'
        ml.forgetting()
        #print ml.classify(d, [a, b, c])#, 1)
        ml.increase_samples_category([sample, b], d)
        #ml.display_time()
        #print 'ml.forgetting'
        ml.forgetting()
        #ml.display_time()
        #ml.display_memory()
        #print 'ml.forgetting'
        ml.forgetting()
        #ml.display_time()
        #ml.display_memory()
        self.assertEqual(ml.classify(sample, [a, b, c]), 0)
        self.assertEqual(ml.classify(a, [sample, b, c]), 0)
        self.assertEqual(ml.classify(b, [a, sample, c]), 1)
        self.assertEqual(ml.classify(c, [a, b, sample]), 2)
if __name__ == '__main__':
    unittest.main()
    
    