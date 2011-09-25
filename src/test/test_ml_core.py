import sys
sys.path.append('../')
import unittest
from cog_abm.ML.core import *


animals = ["dog", "cat","lion","duck","python:)"]


class TestMlCore(unittest.TestCase):
    
    def setUp(self):
        pass


class TestNumericAttribute(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_getting_value(self):
        na = NumericAttribute()
        for i in xrange(10):
            self.assertEqual(i, na.get_value(i))



class TestNominalAttribute(unittest.TestCase):
    
    def setUp(self):
        self.symbols = animals
        self.na = NominalAttribute(self.symbols)
    
    
    def test_getting_value(self):
        na = NominalAttribute(self.symbols)
        for i,s in enumerate(self.symbols):
            self.assertEqual(s, na.get_value(i))
            self.assertEqual(s, na.get_symbol(i))
            self.assertEqual(i, na.get_idx(s))



class TestSample(unittest.TestCase):
    
    def setUp(self):
        self.meta = [NumericAttribute(), NominalAttribute(animals)]
        self.sample = Sample([1.2, self.meta[1].get_idx("dog")], self.meta)
        self.meta_cl = NominalAttribute(animals)
        self.sample_cl = Sample([100, self.meta[1].get_idx("cat")], self.meta,
                                self.meta_cl.get_idx("duck"), self.meta_cl)


    def test_basic(self):
        self.assertIsNone(self.sample.get_cls())
        self.assertEqual(self.sample_cl.get_cls(), "duck")
        
        self.assertEqual(self.sample.get_values(), [1.2, "dog"])
        self.assertEqual(self.sample_cl.get_values(), [100, "cat"])
