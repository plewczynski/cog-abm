"""
Provides tools to measure performance of agents/classifiers
"""
from tools import abstract


class FitnessMeasure(object):
    
    def add_payoff(self, payoff, weight = 1.):
        abstract()

#    This is optional- needed only when buffering
    def update_removed(self, payoff, weight = 1.):
        abstract()
    
    def get_fitness(self):
        abstract()


#class SimpleFitnessMeasure(FitnessMeasure):
#    
#    def __init__(self, update_fun, current_fun, initial_data,
#                                                    update_removed = None):
#        # for simplicity current_fun is given
#        # it would be faster to calculate current_value with update
#        # but this can be achieved - just put it in storage ;) 
#        self.storage = initial_data
#        self.update_fun = update_fun
#        self.current_fun = current_fun
#        self.update_removed = update_removed
#    
#    def add_payoff(self, payoff, weight = 1.):
#        self.storage = self.update_fun(self.storage, payoff, float(weight))
#    
#    def update_removed(self, payoff, weight = 1.):
#        self.storage = self.update_removed(self.storage, payoff, 
#                                                            float(weight))
#    
#    def get_fitness(self):
#        return self.current_fun(self.storage)
#
# I though that this might be nice prove of usefulness of above class...
# but it is 
#class AverageFitnessMeasure(SimpleFitnessMeasure):
#    
#    def __init__(self):
#        #             sum, weight sum
#        def_storage = (0., 0.)
#        update = lambda s, p, w: (s[0]+w*p, s[1]+w)
#        current = lambda (s, ws): s / ws
#        super(AverageFitnessMeasure, self).\
#                __init__(update, current, def_storage)
        

class BufferedFitnessMeasure(FitnessMeasure):
    
    def __init__(self, fm, k):
        from Queue import deque
        self.fm = fm
        self.values = deque()
        self.k = k
    
    def add_payoff(self, payoff, weight = 1.):
        if len(self.values)>=self.k:
            self.fm.update_removed(*self.values.popleft())
            
        self.values.append((payoff, weight))
        self.fm.add_payoff(payoff, weight)
    
#    def update_removed(self, payoff, weight = 1.):
#        # TODO: I'm not sure if any thing should be here
#        # because update_removed is called only before add_payoff and 
#        # there happens everything that needs to be done
#        # Let say that double buffering is not supported ;) 
#        pass
    
    def get_fitness(self):
        return self.fm.get_fitness()
    

class AverageFitnessMeasure(FitnessMeasure):
    
    def __init__(self):
        self.sum = 0.
        self.wsum = 0.
    
    def add_payoff(self, payoff, weight = 1.):
        self.sum += float(weight) * payoff
        self.wsum += weight
    
    def update_removed(self, payoff, weight = 1.):
        # little trick :)
        self.add_payoff(payoff, -weight)

    def get_fitness(self):
        if self.wsum == 0.:
            return 0.
        return self.sum / self.wsum
    

def get_buffered_average(k):
    return BufferedFitnessMeasure(AverageFitnessMeasure(), k)

