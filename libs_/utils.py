"""
this .py file contains some miscellaneous methods.

"""


def tuple_(g):
    g = g[1:-1]
    g = g.split(',')
    d = tuple([int(i) for i in g])
    return d

