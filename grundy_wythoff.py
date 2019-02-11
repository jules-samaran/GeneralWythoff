import numpy as np


def grundy_wythoff(size=50):
    # returns the grundy numbers of all positions on the Wythoff board game
    table = -1 * np.ones((size, size))
    table[0][0] = 0 # not necessary
    for i in range(size):
        for j in range(size):
            table[i][j] = mex([table[pos[0]][pos[1]] for pos in accessible(np.array([i, j]))])
    return table.astype(int)


def mex(l):
    # returns the smallest positive integer not present in the given sequence
    return min(np.delete(np.arange(len(l) + 1), np.unique(l)))


def accessible(position):
    k = min(position[0], position[1])
    diag = np.array([position - i for i in range(1, k + 1)])
    down = np.array([np.array([position[0], position[1] - i]) for i in range(1, position[1] + 1)])
    left = np.array([np.array([position[0] - i, position[1]]) for i in range(1, position[0] + 1)])
    to_keep = []
    for l in [left, down, diag]:
        if len(l) > 0:
            to_keep.append(l)
    access = np.concatenate(to_keep) if len(to_keep) > 0 else []
    return access
