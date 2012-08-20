"""
Module with useful functions and constants
"""
import math

from itertools import imap, izip, chain

import numpy

argmax = lambda funct, items: max(izip(imap(funct, items), items))
argmin = lambda funct, items: min(izip(imap(funct, items), items))

fst = lambda x: x[0]
snd = lambda x: x[1]
ident = lambda x: x


def ext(l, i):
    return [x[i] for x in l]


def iext(l, i):
    return (x[i] for x in l)


def iflatten(iterable_of_iterables):
    return chain.from_iterable(iterable_of_iterables)


def flatten(iterable_of_iterables):
    return list(iflatten(iterable_of_iterables))


def def_value(v, default):
    return v or default


def abstract():
    """A method that simulates abstraction of a method.
    """
    import inspect
    caller = inspect.getouterframes(inspect.currentframe())[1][3]
    raise NotImplementedError(caller + ' must be implemented in subclass')


def get_progressbar(title=None):
    from progressbar import ProgressBar, Percentage, Bar, ETA, Timer
    widgets = [Percentage(), Timer(), Bar(), ETA()]
    if title is not None:
        widgets = [title] + widgets

    return ProgressBar(widgets=widgets)


def avg(l):
    if l:
        return numpy.mean(l)
    return 0.


def stdev(l):
    return numpy.std(l)


def calc_std(l):
    if l:
        l = numpy.array(l)
        return (l.mean(), l.std())
    return (0., 0.)


def calc_auc(curve):
    ''' Calculates area under the curve (AUC)
    '''
    def trapezoid_area(p1, p2):
        (x1, y1), (x2, y2) = ((float(x), float(y)) for x, y in (p1, p2))
        return abs(x1 - x2) * (y1 + y2) / 2.
    return math.fsum((trapezoid_area(p1, p2)
                    for p1, p2 in izip(curve, curve[1:])))


def check_if_module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True
