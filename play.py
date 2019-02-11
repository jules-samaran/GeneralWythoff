from nim_table import *
from grundy_wythoff import grundy_wythoff
import numpy as np


class Game():
    def __init__(self, size=50):
        self.size = size
        self.position = None
        self.stop = 0

    def get_grundy(self, current_pos=True, positions=None):
        pass

    def get_accessible(self):
        pass

    def play(self):
        r""" Interacts with one of the players to decide his next move in the game
        :return: the state of the game, 1 if it is over and 0 otherwise
        """
        print("Your current position on the board game is: ")
        print(self.position)
        print("You can go to the following positions:")
        access = self.get_accessible()
        for i, pos in enumerate(access):
            print('Choice %s' % str(i))
            print(pos)
        choice = int(input("Which choice do you prefer?"))
        self.position = access[choice]
        if len(self.get_accessible()) == 0:
            print("This sub-game is over")
            return 1
        return 0


class Wythoff(Game):
    def __init__(self, size=50):
        super().__init__(size)
        self.position = np.array([size - 1, size - 1])
        self.grundy_table = grundy_wythoff(size)

    def get_accessible(self):
        r""" returns all the positions a player can reach with one move from his current position
        """
        k = min(self.position[0], self.position[1])
        diag = np.array([self.position - i for i in range(1, k+1)])
        down = np.array([np.array([self.position[0], self.position[1] - i]) for i in range(1, self.position[1] + 1)])
        left = np.array([np.array([self.position[0] - i, self.position[1]]) for i in range(1, self.position[0] + 1)])
        to_keep = []
        for l in [left, down, diag]:
            if len(l) > 0:
                to_keep.append(l)
        access = np.concatenate(to_keep) if len(to_keep) > 0 else []
        return access

    def get_grundy(self, current_pos=True, positions=None):
        r"""
        :param current_pos: a bool that indicates whether it's the current position we are interested in
        :param positions: can be any set of positions whose grundy numbers we are interested in, none are specified
        and if current_pos is False it will be the accessible positions from the current position
        :return: the array of grundy numbers of a set of positions or a single integer if there is a single position
        """
        if current_pos:
            return self.grundy_table[self.position[0]][self.position[1]]
        elif positions is None:
            positions = self.get_accessible()
        return np.array([self.grundy_table[pos[0]][pos[1]] for pos in positions])


class Nim(Game):
    def __init__(self, size=50):
        super().__init__(size)
        self.position = size - 1

    def get_accessible(self):
        r""" returns all the positions a player can reach with one move from his current position
        """
        return(np.arange(self.position))

    def get_grundy(self, current_pos=True, positions=None):
        r""" Gives the grundy numbers of a certain set of positions
        :param current_pos: a bool that indicates whether it's the current position we are interested in
        :param positions: can be any set of positions whose grundy numbers we are interested in, none are specified
        and if current_pos is False it will be the accessible positions from the current position
        :return: the array of grundy numbers or a single integer if there is a single position
        """
        if current_pos:
            return self.position
        elif positions is None:
            positions = self.get_accessible()
        return positions
        
        
class Game_play(Game):
    def __init__(self, n_nim=1, size_nim=50, size_wythoff=50):
        self.game_sum = [Wythoff(size_wythoff)] + [Nim(size_nim) for i in range(n_nim)]
        self.table_nim = nim_table(3)

    def get_grundy(self, current_pos=True, positions=None):
        r""" Gives the grundy numbers of a certain set of positions
        :param current_pos: a bool that indicates whether it's the current position we are interested in
        :param positions: can be any set of positions whose grundy numbers we are interested in, none are specified
        and if current_pos is False it will be the accessible positions from the current position
        :return: the array of grundy numbers or a single integer if there is a single position
        """
        return self.general_nim_sum(np.concatenate([game.get_grundy(current_pos=current_pos, positions=positions)
                                                    for game in self.games]).ravel())

    def play(self, with_strategy=False):
        r"""Interacts with one of the players to decide his next move in the game

        :param with_strategy:
        :return: the state of the game, 1 if it is over and 0 otherwise
        """
        print("Your current position on the Wythoff board game is: ")
        print(self.game_sum[0].position)
        for k, game in enumerate(self.game_sum[1:]):
            print("Your current position in the Nim game number %i is: " %k)
            print(game.position)
        if with_strategy:
            self.find_zero_grundy()
        if not self.game_sum[0].stop:
            print("Type w if you wish to move on the Wythoff game board")
        print("Type i if i is the number of the Nim game in which you want to move")
        print("You cannot move in any subgames where the final position has already been reached")
        choice = input("What is your play?")
        if choice == 'w':
            self.game_sum[0].stop = self.game_sum[0].play()
        if choice in np.arange(len(self.game_sum)- 1).astype(str):
            self.game_sum[int(choice) + 1].stop = self.game_sum[int(choice) + 1].play()
        if not np.array([len(game.get_accessible()) == 0 for game in self.game_sum]).all():
            return 0
        else:
            return 1

    def general_nim_sum(self, l):
        r"""  Computes recursively the nim sum of a sequence of integers

        :param l:  list of integers to be nim-summed
        :return: an integer
        """
        if len(l)<2:
            print('You must give at least two arguments')
            return None
        if len(l) == 2:
            return self.table_nim[l[0]][l[1]]
        else:
            sub_sum = self.table_nim[l[0]][l[1]]
            tail = l[2:]
            tail.append(sub_sum)
            return self.general_nim_sum(tail)

    def find_zero_grundy(self):
        r"""  Finds if it exists a position accessible with one move from the current position and
        whose grundy number is 0

        :return: None but prints messages for the player using this strategy
        """
        current_grundys = [game.get_grundy() for game in self.game_sum]
        if self.general_nim_sum(current_grundys) == 0:
            print("You are already on a position whose grundy number is 0 so you can't use this winning strategy!")
            return None
        else:
            for i in range(len(self.game_sum)):
                objective = self.general_nim_sum(np.delete(current_grundys, i))
                accessible_grundy = self.game_sum[i].get_grundy(current_pos=False)
                for k in range(len(self.game_sum[i].get_accessible())):
                    if accessible_grundy[k] == objective:
                        if i == 0:
                            subgame = 'wythoff game'
                        else:
                            subgame = 'Nim game number %i' %(i - 1)
                        good_pos = str(self.game_sum[i].get_accessible()[k])
                        print("if you go to the position %s in the %s" %(good_pos, subgame))
                        print("You will be on a position with a zero grundy number in the global game")
                        return None


def run():
    r""" The main function that simulates a match between two players with this game

    :return:  Nothing
    """
    n = 0
    game = Game_play()
    while 1>0:
        player = n % 2
        print("It is Player %i 's turn to play!" %(player + 1))
        stop = game.play(with_strategy=not bool(player))
        if stop:
            print("Player %i has won!!" %(player + 1))
            break
        n += 1
