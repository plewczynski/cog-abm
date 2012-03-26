"""Makes tests and simple simulations easier"""

from ..core.network import Network
from ..core.interaction import Interaction
from ..core.agent import Agent

from pygraph.algorithms.generators import generate


def generate_simple_network(agents):
    n = len(agents)
    network = Network(generate(n, n*(n-1) // 2, directed = False))

    for i, a in enumerate(agents):
        network.add_agent(a, i)
#        network.add_agent(a, i, a)
#        network.add_agent(a, i, str(i))
    return network
    

  


def generate_network_with_agents(n):
    agents = [Agent(aid=i) for i in xrange(n)]
    return (generate_simple_network(agents), agents)





class SimpleInteraction(Interaction):
    """ Very simple interaction. Just prints agents involved and takes time.
    """
    
    
    def __init__(self, num_agents = 2):
        self._num_agents = num_agents
    
    
    def num_agents(self):
        return self._num_agents
    
    
    def interact(self, *agents):
        import os
        print "Interaction with: "+str(agents)+ "  in: "+ str(os.getpid())
        for i in xrange(10**5):
            i**0.5
        return [i**0.1 for i in xrange(len(agents))]
        


from cog_abm.ML.core import Classifier

def extract_classes(samples):
    return list(set((s.get_cls() for s in samples)))

class SimpleClassifier(Classifier):

    def classify_pval(self, sample):
        return self.classify(sample), 1.

    def class_probabilities(self, sample):
        d = {}
        for c in self.classes:
            d[c] = 0.
        d[self.classify(sample)] = 1.
        return d

    def train(self, samples):
        self.classes = extract_classes(samples)

class PerfectClassifer(SimpleClassifier):
    """ If given sample has class, it returns it
    """
    
    def classify(self, sample):
        return sample.get_cls()


class StupidClassifer(SimpleClassifier):
    """ Always returns the same class
    """

    def __init__(self, cls = 0):
        self.cls = str(cls)

    def classify(self, sample):
        return self.cls


