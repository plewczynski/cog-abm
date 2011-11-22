"""
This module implements measurements used in evaluating the outcome of the
experiment.
"""
import math
from itertools import ifilter, imap, combinations


window_size = 50
#window_size = 1<<50

def DS_A(agent):

	w = filter(lambda (id, w):id == "DG", agent.inter_res)

	if len(w) == 0:
		return 0.
	
	w = w[max(0, len(w)-window_size) : ]
	return math.fsum(imap(lambda r:r[1], w))/len(w)


def DS(agents, it):
	if it == 0:
		return 0
	return math.fsum([DS_A(a) for a in agents])/len(agents)



def CS_A(agent):

	w = filter(lambda (id, w):id == "GG", agent.inter_res)

	if len(w) == 0:
		return 0.
	
	w = w[max(0, len(w)-window_size) : ]
	return math.fsum(imap(lambda r:r[1], w))/len(w)

def CS(agents, it):
	if it == 0:
		return 0
	return math.fsum([CS_A(a) for a in agents])/len(agents)




def ru_dist(ru1, ru2):
	#print math.log(ru1[1], 0.8), math.log(ru2[1], 0.8)
	#return math.log(ru1[1], 0.001)*math.log(ru2[1], 0.001)*ru1[0].dist(ru2[0])
	#return ru1[1]*ru2[1]*ru1[0].dist(ru2[0])
	#what was in Steels:
	return ru1[0].dist(ru2[0])

def d(A, B, m):
	
	s1 = math.fsum([min([m(a, b) for b in B]) for a in A])
	s2 = math.fsum([min([m(a, b) for a in A]) for b in B])

	return (s1+s2)/(len(A) * len(B))
	#/math.log((len(A) * len(B))+1)


# c & cp are lists of (ReactiveUnit, weight)
def d_category(c, cp):
	return d(c, cp, ru_dist)
	

# normaly there would be agents
# a & ap are lists of lists of (ReactiveUnit, weight) - each inner list represents one adaptive network
def D(a, ap):
	return d(a, ap, d_category)

def cv(agents, it):
	if it == 0:
		return None# it's fine on graph

#	ag_centres = [tuple(
#	                    [tuple(
#							[wru for wru in an.units])
#						for _, an in a.state.classifier.categories.iteritems()]
#				) for a in agents]
#	ag_centres = tuple(ag_centres)
	ag_centres = [
	                    [		[wru for wru in an.units]
						for _, an in a.state.classifier.categories.iteritems()]
				 for a in agents]

	
	suma = math.fsum(D(a1, a2) for a1, a2 in combinations(ag_centres, 2) if len(a1)>0 and len(a2)>0)
	#return suma
	#return suma*2/(len(agents) * (len(agents)-1))
	return suma*2/(len(agents) * (len(agents)-1))
#	return (len(agents) * (len(agents)-1))/(suma*2)










def mcv(agents_centres):
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
	#To test some new distances - should use weights!
	import sys
	sys.path.append("../")
	from steels.steels_experiment import *
	rus = [(ReactiveUnit([x, x, x]), 1./(x+1)) for x in xrange(3)]
	rus2 = [(ReactiveUnit([x+1, x+1, x+1]), 1./(x+1)) for x in xrange(3)]
	print rus
	print rus2
	print d_category(rus, rus2)
	rus = [(ReactiveUnit([x, x, x]), 1.) for x in xrange(3)]
	rus2 = [(ReactiveUnit([x+20, x-19, x+18]), 1.) for x in xrange(3)]
	print d_category(rus, rus2)
	
