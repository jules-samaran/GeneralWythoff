from nim_table import *
from grundy_wythoff import grundy_wythoff
from play import *
import numpy as np


def test_nim():
    nim = Nim(5)
    while 1 > 0:
        state = nim.play()
        if state:
            print('test Nim ok')
            break


def test_wythoff():
    wythoff = Wythoff(5)
    while 1 > 0:
        state = wythoff.play()
        if state and wythoff.position == np.array([0, 0]):
            print('test Wythoff ok')
            break


def test_nim_table():
    ## We test that the values computed in the table are correct for a
    ## randomly sampled set of numbers
    t = nim_table(3)
    tries_x = np.random.choice(np.arange(len(t)), len(t)//4, replace=False)
    tries_y = np.random.choice(np.arange(len(t)), len(t)//4, replace=False)
    for a, b in zip(tries_x, tries_y):
        assert a^b == t[a, b], "There are errors in the table"
    print("Test table of Nim sum ok")


def test_global_game():
    n = 0
    game = Game_play(n_nim=2, size_nim=5, size_wythoff=5)
    while 1 > 0:
        player = n % 2
        stop = game.play(with_strategy=not bool(player))
        if stop:
            print("Player %i has won!!" % (player + 1))
            break
        n += 1


test_nim()
test_wythoff()
test_nim_table()
test_global_game()
