import sys
sys.path.append('../')
import unittest
from cog_abm.extras.lexicon import *


class TestWords(unittest.TestCase):
	
	def test_simple(self):
		Syllable.set_allowed_syllables(["a", "b", "z", "y", "x"])
		Word.set_max_len(3)
		w = Word.get_random()
		w2 = Word.get_random_not_in(set([w]))
		self.assertNotEqual(w, w2)
	
	def test_equalities(self):
		Syllable.set_allowed_syllables(["a", "b", "z", "y", "x"])
		Word.set_max_len(3)
		w1 = Word(["a", "b"])
		w2 = Word(["a", "b"])
		self.assertEqual(w1, w2)
		self.assertNotEqual(w1, Word(["a", "z"]))
		self.assertNotEqual(w2, Word(["a", "z"]))
		

class TestLexicon(unittest.TestCase):
	
	def setUp(self):
		self.words = []
		for _ in xrange(10):
			self.words.append(Word.get_random_not_in(self.words))
		
		self.l = Lexicon()
	
	
	def test_1(self):
		wl = [self.l.add_element(i) for i in xrange(10)]

		for w in wl:
			self.assertTrue(self.l.category_for(w) in range(10))
		

	def test_increase_word(self):
		wl = [self.l.add_element(i) for i in xrange(10)]
		print [str(w) for w in wl]
		self.l.inc_dec_words(1, wl[1])
		self.assertTrue(self.l.word_for(1) == wl[1])
		
		
	def test_not_present_values(self):
		self.assertEqual(None, self.l.word_for(0))
	
	
	def test_decrasing_and_increasing_categories(self):
		w = Word.get_random()
		self.l.add_element(0, w, 0.8)
		self.l.add_element(1, w, 0.7)
		self.l.add_element(1, Word.get_random_not_in([w]), 0.1)
		self.assertEqual(0, self.l.category_for(w))
		for _ in xrange(2):
			self.l.decrease(0, w)
		self.assertEquals(1, self.l.category_for(w))
		
		for _ in xrange(1):
			self.l.inc_dec_categories(0, w)
		self.assertEqual(0, self.l.category_for(w))


	def test_decrasing_and_increasing_word(self):
		w = Word.get_random()
		w2 = Word.get_random_not_in([w])
		self.l.add_element(0, w, 0.8)
		self.l.add_element(0, w2, 0.7)
		self.assertEqual(w, self.l.word_for(0))
		for _ in xrange(1):
			self.l.inc_dec_words(0, w2)
		self.assertEquals(w2, self.l.word_for(0))
		
		
	def test_str_repr(self):
		w = Word.get_random()
		self.l.add_element(0, w, 0.8)
		self.l.add_element(1, w, 0.7)
		self.assertIn(str(w), str(self.l))
		self.assertIn(str(0.7), str(self.l))
		self.assertIn(str(0.8), str(self.l))
		
	
if __name__ == '__main__':
	unittest.main()
	
