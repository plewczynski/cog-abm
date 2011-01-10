import sys
sys.path.append('../')
import unittest
from steels.direct_classif import *
from steels.simple_classif import *

class TestMultiClassif(unittest.TestCase):
    def test_knn(self):
        #test learning
        sample = [1, 2, 3]
        a = [2, 3, 4]
        b = [3, 4, 5]
        c = [0, 1, 4]
        d = [2.5, 3.5, 4.5]
        #print 'Creating DirectClassifier(SimpleKnnIntClassifier)'
        ml = DirectClassifier(SimpleKnnIntClassifier)
        #print 'adding a new category'
        ml.add_category(sample, [a, b, c])
        self.assertEqual(ml.classify(sample, [a, b, c]), 0)
        self.assertEqual(ml.classify(a, [sample, b, c]), 1)
        self.assertEqual(ml.classify(b, [a, sample, c]), 1)
        self.assertEqual(ml.classify(c, [a, b, sample]), 0)
        ml.add_category(c, [sample, b, a])
        #print ml.classify(sample, [c, b, a])#, 0)
        #print ml.classify(a, [sample, b, c])#, 0)
        #print ml.classify(b, [sample, a, c])#, 0)
        #print ml.classify(c, [sample, b, a])#, 1)
        #test forgetting:
        #ml.display_time()
        ml.forgetting()
        #ml.display_time()
        ml.forgetting()
        #print ml.classify(d, [a, b, c])#, 1)
        ml.increase_samples_category([sample, b], d)
        #ml.display_time()
        #ml.forgetting()
        #ml.display_time()
        #ml.display_memory()
        #print ml.classify(sample, [c, b, a])#, 0)
        #print ml.classify(a, [sample, b, c])#, 0)
        #print ml.classify(b, [sample, a, c])#, 0)
        #print ml.classify(c, [sample, b, a])#, 1)
        ml.forgetting()
        #ml.display_time()
        #ml.display_memory()
        #print '****************************************'
        self.assertEqual(ml.count_categories(), 3)
        self.assertEqual(ml.classify(sample, [a, b, c]), 0)
        self.assertEqual(ml.classify(a, [sample, b, c]), 1)
        self.assertEqual(ml.classify(b, [a, sample, c]), 1)
        self.assertEqual(ml.classify(c, [a, b, sample]), 2)
if __name__ == '__main__':
    unittest.main()
    
    