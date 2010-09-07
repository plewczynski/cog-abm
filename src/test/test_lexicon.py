import sys
sys.path.append('../')
import unittest
from cog_abm.extras.lexicon import *


class TestLexicon(unittest.TestCase):
	
	def setUp(self):
		self.words = []
		for i in xrange(10):
			self.words.append(Word.get_random_not_in(self.words))
	
	
	def test_1(self):
		l = Lexicon()
		wl = [l.add_element(i) for i in xrange(10)]

		for w in wl:
			i = l.category_for(w)
			print i
			self.assertTrue(i in range(10))
		

	
	def test_increase_word(self):
		l = Lexicon()
		wl = [l.add_element(i) for i in xrange(10)]
		print [str(w) for w in wl]
		l.increase_word(1, wl[1])
		print l
		self.assertTrue(l.word_for(1) == wl[1])
		
		
	
	
	
if __name__ == '__main__':
    unittest.main()
