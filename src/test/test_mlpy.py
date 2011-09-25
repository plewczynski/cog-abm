import sys
sys.path.append('../')
import unittest
import numpy as np
import mlpy

class TestMlpy(unittest.TestCase):
    def test_knn_fda(self):
        #knn:
        xtr = np.array([[1.0, 2.0, 3.1, 1.0], # first sample
        [1.0, 2.0, 3.0, 2.0], # second sample
        [1.0, 2.0, 3.1, 1.0]]) # third sample
        ytr = np.array([1, -1, 1]) # classes
        knn = mlpy.Knn(k = 1) # initialize knn class
        knn.compute(xtr, ytr) # compute knn
        knn.predict(xtr) # predict knn model on training data
        xts = np.array([4.0, 5.0, 6.0, 7.0]) # test point
        self.assertEqual(knn.predict(xts), -1) # predict knn model on test point
        #fda:
        sample = [1, 2, 3]
        a = [2, 3, 4]
        b = [3, 4, 5]
        c = [0, 1, 4]
        d = [2.5, 3.5, 4.5]
        xtr = np.array([sample, a, b, c])
        ytr = np.array([1, -1, -1, -1]) # classes
        fda = mlpy.Fda() # initialize Fda class
        self.assertEqual(fda.compute(xtr, ytr), 1) # compute Fda
        test_point = np.array([1, 2, 3])
        self.assertEqual(fda.predict(test_point), 1)
        #fda.realpred
        test_point = np.array([4, 5, 6])
        self.assertEqual(fda.predict(test_point), -1)
        #fda.realpred
        test_point = np.array([10, 11, 23])
        self.assertEqual(fda.predict(test_point), -1)
        #fda.realpred
        test_point = np.array([1, 2.5, 3])
        self.assertEqual(fda.predict(test_point), 1)
        #fda.realpred


if __name__ == '__main__':
    unittest.main()