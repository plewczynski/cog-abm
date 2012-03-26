"""
Module with useful functions and constants
"""
import math
from itertools import imap, izip

argmax = lambda funct, items: max(izip(imap(funct, items), items))
argmin = lambda funct, items: min(izip(imap(funct, items), items))

def_value = lambda v, default: v or default


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
        return math.fsum(l) / len(l)
    return 0.

def stdev(l, av=None):
    if not l:
        return 0.
    if av is None:
        av = avg(l)
    avgsq = avg([x**2. for x in l])
    return max(0., (avgsq - av**2.))**.5

def calc_std(l):
    if l:
        av = avg(l)
        return (av, stdev(l, av))
    return (0., 0.)
