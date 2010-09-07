
import math
import random



"""
This module implements measurements used in evaluating the outcome of the
experiment.
"""
import math


default_sliding_window_size = 5.


def DSA( agents_results, sliding_window_size = default_sliding_window_size):
    """ Returns cumulative success for specified agent and with
    specified sliding_window_size.
    """
    
    cumulative_success = 0.
    if len(agents_results) <= sliding_window_size:
        return float(sum(agents_results)) / len(agents_results)
    else:
        for i in \
                range(len(self.agents_results) - \
                sliding_window_size,len(agents_results)):
                    cumulative_success += \
                                agents_results[i]
    return float(cumulative_success) / sliding_window_size


def DS(multi_agents_results, sliding_window_size = 
            default_sliding_window_size):
    """ Returns average success of population
    """
    cumulative_success_pop = math.fsum([DSA(i,sliding_window_size)\
                                        	for i in multi_agents_results])
    return cumulative_success_pop / len(multi_agents_results)



def cv(agents_centres):
    """ calculates the category varianve between agents categorical split
    @agents_centres: list of lists of centre value = list of classes:
            e.g.: [[c1, c2, c3], [c1, c2], [c1], [c1, c2, c3, c4]]
    @return: number denoting the variance value
    """
    cat_var = 0.
    for i in range(1, len(agents_centres)):
        for j in range(i):
            cat_var += cat_dist(agents_centres[i], agents_centres[j])
    cat_var /= len(agents_centres) * (len(agents_centres)-1)
    cat_var *= 2
    return cat_var


def cv_prim(agents_centres1, agents_centres2):
    """ calculates the category varianve between agents categorical split
    @agents_centres1: list of lists of centre value:
            e.g.: [[c1, c2, c3], [c1, c2], [c1], [c1, c2, c3, c4]]
    @agents_centres2: list of lists of centre value:
            e.g.: [[c1, c2, c3], [c1, c2], [c1], [c1, c2, c3, c4]]
    @return: number denoting the variance value
    """
    cat_var = 0.
    cat_var = math.fsum([cat_dist(x,y) for x in 
                agents_centres1 for y in agents_centres2])
    cat_var /= len(agents_centres1) * (len(agents_centres2))
    return cat_var


def cat_dist(set1, set2):
    """ returns distance between 2 given sets
    """
    sum1 = 0.
    for e1 in set1:
        h1 = min(basic_dist(e1, e2) for e2 in set2)
        sum1 += h1
    
    sum2 = 0
    for e2 in set2:
        h2 = min(basic_dist(e2, e1) for e1 in set1)
        sum2 += h2
    return 1.0 * (sum1 + sum2) / (len(set1) * len(set2))


def basic_dist(set1, set2):
    """
    """
    return math.sqrt( sum((e1 - e2)**2 \
            for e1, e2 in zip(set1, set2)))


if __name__ == '__main__':
    pass
