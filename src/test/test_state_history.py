#import sys
#sys.path.append('../')
#import unittest
#from cog_abm.agent.state import *
#
#
#class TestStateHistory(unittest.TestCase):
#
#       def setUp(self):
#               pass
#
#       def test_get_state(self):
#               """
#               Does StateHistory returns state properly.
#               """
#               set = range(10)
#               self.states = set
#               for i in set:
#                       self.assertTrue(self.states.get_state(i) == i)
#
#       def test_add_state(self):
#               """
#               Does StateHistory properly adds new state to the set.
#               """
#               set = range(10)
#               self.states = set
#               add_state(12)
#               self.assertEqual(self.states[len(set) + 1], 12)
#
#       def test__len__(self):
#               """
#               Does StateHistory returns proper size of set when requested by len()
#               """
#               set = range(10)
#               self.states = set
#               self.assertTrue(len(self) == 10)
#               pass
#
#
#if __name__ == '__main__':
#    unittest.main()
