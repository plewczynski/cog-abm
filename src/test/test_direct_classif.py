import sys
sys.path.append('../')
import unittest
from cog_abm.ML.direct_classif import *
from cog_abm.ML.simple_classif_mlpy import *

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
        ml.add_category(sample)
        self.assertEqual(ml.classify(sample), 0)
        self.assertEqual(ml.classify(a), 0)
        self.assertEqual(ml.classify(b), 0)
        self.assertEqual(ml.classify(c), 0)
        ml.add_category(c)
        #print ml.classify(sample, [c, b, a])#, 0)
        #print ml.classify(a)#, 0)
        #print ml.classify(b, [sample, a, c])#, 0)
        #print ml.classify(c, [sample, b, a])#, 1)
        #test forgetting:
        #ml.display_time()
        ml.forgetting()
        #ml.display_time()
        ml.forgetting()
        #print ml.classify(d)#, 1)
        ml.increase_samples_category(d)
        #ml.display_time()
        #ml.forgetting()
        #ml.display_time()
        #ml.display_memory()
        #print ml.classify(sample, [c, b, a])#, 0)
        #print ml.classify(a)#, 0)
        #print ml.classify(b, [sample, a, c])#, 0)
        #print ml.classify(c, [sample, b, a])#, 1)
        ml.forgetting()
        #ml.display_time()
        #ml.display_memory()
        #print '****************************************'
        self.assertEqual(ml.count_categories(), 2)
        self.assertEqual(ml.classify(sample), 0)
        self.assertEqual(ml.classify(a), 0)
        self.assertEqual(ml.classify(b), 0)
        self.assertEqual(ml.classify(c), 1)
if __name__ == '__main__':
    unittest.main()
