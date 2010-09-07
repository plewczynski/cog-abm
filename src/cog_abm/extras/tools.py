

from itertools import imap, izip

argmax = lambda funct, items: max(izip(imap(funct, items), items))

argmin = lambda funct, items: min(izip(imap(funct, items), items))
