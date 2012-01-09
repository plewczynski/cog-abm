import unittest

from steels_experiment import *
from cog_abm.ML.core import Sample

class TestReactiveUnit(unittest.TestCase):
	
	def setUp(self):
		self.N = 100
		
	
	def test_values(self):
		
		for _ in xrange(self.N):
			n = random.randint(3, 6)
			w = [random.randint(0, 10) for _ in xrange(n)]
			z = ReactiveUnit(w)
			self.assertEqual(1,  z.value_for(w))
		
		for _ in xrange(self.N):
			n = random.randint(3, 6)
			m = [random.randint(0, 10) for _ in range(n)]
			z = ReactiveUnit(m)
			w = [random.randint(0, 10) for _ in range(n)]
			self.assertTrue(0<= z.value_for(w)<=1)

	def test_comparision(self):
		for _ in xrange(self.N):
			n = random.randint(3, 6)
			w1 = [random.randint(0, 10) for _ in range(n)]
			
			w2 = w1
			while w2 == w1:
				w2 = [random.randint(0, 10) for _ in range(n)]
				
			self.assertNotEqual(ReactiveUnit(w1),  ReactiveUnit(w2))
			
		for _ in xrange(self.N):
			n = random.randint(3, 6)
			w1 = [random.randint(0, 10) for _ in range(n)]
			w2 = [x for x in w1]
			self.assertEqual(ReactiveUnit(w1),  ReactiveUnit(w2))
		
		self.assertFalse(ReactiveUnit([1, 2, 3]) == 5)
	
	

class TestAdaptiveNetwork(unittest.TestCase):
	
	def setUp(self):
		self.N = 100
		
		self.sample = [(ReactiveUnit([1, 2, 3, 4]), 0.5),  \
								(ReactiveUnit([1, 1, 1, 1]), 0.8), 
								(ReactiveUnit([2, 2, 2, 2]), 0.2), 
								(ReactiveUnit([3, 3, 3, 3]), 1)  ]
		self.an = AdaptiveNetwork(self.sample)
		
	
	
	def test__index_of(self):
		self.assertEqual(-1, self.an._index_of(ReactiveUnit([6, 6, 6])))
		self.assertEqual(1, self.an._index_of(ReactiveUnit([1, 1, 1, 1])))
		self.assertEqual(-1,
						AdaptiveNetwork()._index_of(ReactiveUnit([23, 4])))
	
	
	def test_add_reactive_unit(self):

		for _ in xrange(2):
			self.an.add_reactive_unit(ReactiveUnit([1, 1]))
			self.assertTrue(-1 != self.an._index_of(ReactiveUnit([1, 1])))
			self.assertTrue(-1 == self.an._index_of(ReactiveUnit([1, 1, 1])))
	
	
	def test_reaction(self):
		#TODO: give specific net and specific values
		an = AdaptiveNetwork(self.sample)
		for _ in xrange(self.N):
			pack = [random.randint(0, 10) for _ in range(4)]
			out = np.array([w*ru.value_for(pack) for ru, w in self.sample]).sum()
			self.assertEqual(an.reaction(pack), out)
	
	
	def test__update_units_to_None(self):
		an = AdaptiveNetwork(self.sample)
		an._update_units(lambda u, w:  None)
		self.assertEqual(an.units, [])


	def test__update_units_doubles(self):
		an = AdaptiveNetwork(self.sample)
		an._update_units(lambda u, w: (u,  w*2))
		self.assertTrue(len(an.units) == len(self.sample) and len(an.units)>0)
		self.assertEqual([(u, w*2) for u, w in self.sample], an.units)
	
	
	def test_remove_low_units(self):
		an = AdaptiveNetwork(self.sample)
		an.remove_low_units(0.9)
		self.assertTrue(len(an.units)== 1)
	
	
	def test_incrase_sample(self):
		for ru,  _ in self.sample:
			an = AdaptiveNetwork(self.sample)
			an.increase_sample(ru.central_value)
			wwan = (an.units[an._index_of(ru)])[1]
			
			for wewru, weww in self.sample:
				print weww, (an.units[an._index_of(wewru)])[1]
				self.assertTrue(weww <= (an.units[an._index_of(wewru)])[1])
				if ru == wewru:
					self.assertTrue(weww < wwan or weww == wwan == 1)
	
	
	def test_forgetting(self):#TODO set proper values
		an = AdaptiveNetwork(self.sample)
		an.forgetting()

		for ru, w in an.units:
			for ruw,  ww in self.sample:
				if ruw == ru:
					self.assertTrue(w < ww or ww == 0)




class TestSteelsClassifier(unittest.TestCase):
	
	def setUp(self):
		self.N = 100
		self.samples = [Sample([1, 2, 3, 4]),  Sample([1, 1, 1, 1]), 
					Sample([2, 2, 2, 2]), Sample([3, 3, 3, 3])]
		self.ru = [ReactiveUnit(s.get_values()) for s in self.samples]



	def _init(self):
		self.sc = SteelsClassifier()
		for s in self.samples:
			self.sc.add_category(s)


	def test_add_remove_category(self):
		self._init()
		self.sc.add_category(self.samples[0], 0)
		self.assertTrue(self.sc.categories.has_key(0))
		self.sc.del_category(0)
		self.assertFalse(self.sc.categories.has_key(0))
	
	
	def test_remove_category(self):
		pass
	
	def test_wrong_classify(self):
		self._init()
		self.sc.categories = {}
		self.assertEqual(None, self.sc.classify(self.samples[0]))
	
	def test_classify_for_peeks(self):
		self._init()
		wc = [self.sc.classify(s) for s in self.samples]
		wc.sort()
		self.assertEqual(wc,  range(4))
		
		
	def test_classify_similar(self):
		self._init()
		samples = [Sample([0.9,  0.9,  0.9, 0.9]),  
				Sample([1.1, 1.1, 1.1, 1.1]), Sample([0.9, 1.1, 0.9, 1.1]),
				  Sample([1, 1, 1, 1])]
		wc = [self.sc.classify(s) for s in samples]
		wc.sort()
		self.assertEqual(wc[0],  wc[len(wc)-1])
		
		
class TestSteelsExperiment(unittest.TestCase):
	
	def test_steels_experiment(self):
		pass
