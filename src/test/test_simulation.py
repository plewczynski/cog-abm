import sys
sys.path.append('../')
import unittest
from cog_abm.core.simulation import *


class TestSimulation(unittest.TestCase):

    def setUp(self):
        pass



class TestMultiThreadSimulation(unittest.TestCase):


    def setUp(self):
        from cog_abm.extras.additional_tools import generate_network_with_agents
        from cog_abm.extras.additional_tools import SimpleInteraction
        network, agents = generate_network_with_agents(10)
        self.network = network
        self.agents = agents
        print network.agents
        print network.nodes
        print "___________"
        print agents
        self.interaction = SimpleInteraction(2)


#       def testBasic(self):
#               simulation = MultithreadSimulation(3, graph = self.network,
#                               interaction = self.interaction,  agents = self.agents)
#
#               simulation.run(1000, 50)
