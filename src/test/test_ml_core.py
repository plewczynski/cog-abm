import unittest
from cog_abm.ML.core import *


animals = ["dog", "cat","lion","duck","python:)"]



class TestAttributes(unittest.TestCase):
    
    def setUp(self):
        self.symbols = animals
        self.na = NominalAttribute(self.symbols)


    def test_numeric_attr_getting_value(self):
        na = NumericAttribute()
        for i in xrange(10):
            self.assertEqual(i, na.get_value(i))
    
    
    def test_nominal_attr_getting_value(self):
        na = NominalAttribute(self.symbols)
        for i,s in enumerate(self.symbols):
            self.assertEqual(s, na.get_value(i))
            self.assertEqual(s, na.get_symbol(i))
            self.assertEqual(i, na.get_idx(s))

    
    def test_equality(self):
        self.assertEqual(self.na, NominalAttribute(animals))
        self.assertEqual(self.na, 
                NominalAttribute(["dog", "cat","lion","duck","python:)"]))
        self.assertNotEqual(self.na, NominalAttribute(animals+["donkey"]))
        self.assertEqual(NumericAttribute(), NumericAttribute())
        self.assertNotEqual(self.na, NumericAttribute())
        
    

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
    
    
    def test_equality(self):
        self.assertNotEqual(self.sample, self.sample_cl)
        
        meta = [NumericAttribute(), NominalAttribute(animals)]
        sample = Sample([1.2, meta[1].get_idx("dog")], meta)
        self.assertEqual(self.sample, sample)
        self.assertNotEqual(self.sample, self.sample_cl)
        meta = [NumericAttribute(), NominalAttribute(animals), NumericAttribute()]
        sample = Sample([1.2, meta[1].get_idx("dog"), 3.14], meta)
        self.assertNotEqual(self.sample, sample)
        self.assertNotEqual(self.sample_cl, sample)
        
        meta = [NumericAttribute(), NominalAttribute(animals)]
        sample = Sample([1.2, meta[1].get_idx("cat")], meta)
        self.assertNotEqual(self.sample, sample)
        self.assertNotEqual(self.sample_cl, sample)
        
        sample = Sample([1.3, meta[1].get_idx("dog")], meta)
        self.assertNotEqual(self.sample, sample)
        self.assertNotEqual(self.sample_cl, sample)
        
        sample = Sample([100, self.meta[1].get_idx("cat")], self.meta,
                                self.meta_cl.get_idx("duck"), self.meta_cl)
        self.assertEqual(self.sample_cl, sample)
        self.assertNotEqual(self.sample, sample)
        
        sample = Sample([10.20, self.meta[1].get_idx("cat")], self.meta,
                                self.meta_cl.get_idx("duck"), self.meta_cl)    
        self.assertNotEqual(self.sample, sample)
        self.assertNotEqual(self.sample_cl, sample)
        


class TestSamplePreparation(unittest.TestCase):
    
    def test_loading_arff(self):
        samples = load_samples_arff("test/iris.arff")
        expected_meta = [NumericAttribute() for _ in xrange(4)]
        expected_cls_meta = NominalAttribute(
                    ["Iris-setosa","Iris-versicolor","Iris-virginica"])
        
        sample = samples[0]
        self.assertEqual(sample.meta, expected_meta)
        self.assertEqual(sample.cls_meta, expected_cls_meta)
      
    
    def test_spliting_samples(self):
        samples = load_samples_arff("test/iris.arff")
        import random
        for _ in xrange(100):
            split_ratio = random.random()
            train, test = split_data(samples, split_ratio)
            self.assertEqual(math.ceil(len(samples) * split_ratio), len(train))
            self.assertEqual(len(samples), len(train) + len(test))

