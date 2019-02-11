import numpy as np


def nim_table(n):
    r""" Calculates the table of the Nim sum law for all integers between 0 and 2^(2^n)
    
    :param n: integer that determines the size of the output
    :return: a 2 dimensional array of integers
    """
    t = np.zeros((2,2), int)
    t[0][1] = 1
    t[1][0] = 1
    if n == 0:
        res = t
    else:
        p = 2**(2**(n-1))
        res = np.zeros((p**2,p**2), int)
        t = nim_table(n-1)
        res[:p, :p] = t
        for u in range(p):
            for v in range(p):
                for k in range(p):
                    for l in range(p):
                        res[u + v*p][k + l*p] = t[u][k] + p*t[v][l]
    return res
