"""
Module with useful functions and constants
"""

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
