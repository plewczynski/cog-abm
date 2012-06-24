
from cog_abm.extras.policy import *
import unittest



class TestPolicy(unittest.TestCase):

    def test_get_new_action_data(self):
        policy = Policy()
        try:
            policy._get_new_action_data()
            self.fail("Should raise NotImplementedError")
            policy.get_action(0)
            self.fail("Should raise NotImplementedError")
            policy.add_result(0, 0, 0)
            self.fail("Should raise NotImplementedError")
        except:
            pass


class TestStatisticPolicy(unittest.TestCase):


    def setUp(self):
        self.category = 3
        self.special_action = 42


    def _prepare_policy(self):
        policy = StatisticPolicy()
        self.assertTrue(policy.get_action(self.category) is None)
        for i in xrange(100):
            policy.add_result(self.category, self.special_action, 10)
            policy.add_result(self.category, i, 5)

        return policy


    def test_get_action(self):
        policy = self._prepare_policy()

        il = 0
        for _ in xrange(100):
            if policy.get_action(self.category) == self.special_action:
                il+= 1

        self.assertTrue(70<il)


    def test_actions_vector(self):
        policy = self._prepare_policy()

        self.assertTrue(len(policy.category_actions.keys()) == 1)
        self.assertTrue(len(policy.category_actions[self.category].actions.keys()))
        action_data = policy.category_actions[self.category].actions[self.special_action]
        self.assertTrue(action_data.count == 101)
        self.assertTrue(action_data.sum == 100 * 10+5)
        self.assertTrue(action_data.ssum == 100 * 10*10+5*5)


    def test_random(self):
        policy = self._prepare_policy()
        for _ in xrange(1000):
            if policy.get_action(self.category) != self.special_action:
                return

        self.fail("No random action occured")




if __name__ == '__main__':
    unittest.main()
