#!/bin/python

class State:
    def __init__(self, s: str = ""):
        """
        Create a tic-tac-toe board state

        Mapping from index to spot:
        0 1 2
        3 4 5
        6 7 8

        So "_X_O" would be

        _X_
        O__
        ___

        >>> State("A")
        Traceback (most recent call last):
        ...
        ValueError: invalid characters

        >>> State("XX")
        Traceback (most recent call last):
        ...
        ValueError: illegal board state

        >>> State("__________")
        Traceback (most recent call last):
        ...
        ValueError: too many moves

        """
        if len(s) > 9:
            raise ValueError("too many moves")
        if set(s) - {'X', 'O', '_'} != set():
            raise ValueError("invalid characters")
        move_differences = s.count("X") - s.count("O")
        if move_differences > 1 or move_differences < 0:
            raise ValueError("illegal board state")
        self.s = dict(enumerate(s.ljust(9,"_")))
        self.board = self.to_board()
        self.victory = False
        self.leads_to_win = 0
        self.leads_to_tie = 0
        self.leads_to_loss = 0

    def to_board(self):
        out = [["_" for j in range(3)] for i in range(3)]
        for v in range(9):
           i = v % 3
           j = v // 3
           out[j][i] = self.s[v]
        return out

    def __str__(self):
        """
        >>> print(State())
        ___
        ___
        ___

        >>> print(State("__X"))
        __X
        ___
        ___

        >>> print(State("_OX_OXO_X"))
        _OX
        _OX
        O_X
        """
        return("\n".join(["".join(row) for row in self.board]) + "\n")

    @staticmethod
    def board_to_s(board):
        """
        >>> State.board_to_s(State("X").board)
        'X________'
        """
        return("".join(["".join(row) for row in board]))

    @staticmethod
    def rotate(board):
        """
        0 1 2
        3 4 5
        6 7 8

        -->

        6 3 0
        7 4 1
        8 5 2

        >>> State.rotate(State("X").board)
        [['_', '_', 'X'], ['_', '_', '_'], ['_', '_', '_']]

        >>> State.rotate(State.rotate(State("X").board))
        [['_', '_', '_'], ['_', '_', '_'], ['_', '_', 'X']]
        """
        cw = {0:6, 1:3, 2:0, 3:7, 4:4, 5:1, 6:8, 7:5, 8:2}
        local_s = State.board_to_s(board)
        out = [["_" for j in range(3)] for i in range(3)]
        for v in range(9):
           i = v % 3
           j = v // 3
           out[j][i] = local_s[cw[v]]
        return out

    def rotations(self):
        """
        >>> for r in State("X_O").rotations(): print(r)
        [['X', '_', 'O'], ['_', '_', '_'], ['_', '_', '_']]
        [['_', '_', 'X'], ['_', '_', '_'], ['_', '_', 'O']]
        [['_', '_', '_'], ['_', '_', '_'], ['O', '_', 'X']]
        [['O', '_', '_'], ['_', '_', '_'], ['X', '_', '_']]
        """
        r = self.board
        yield(r)
        for i in range(3):
            r = State.rotate(r)
            yield(r)

    def check_status(self):
        """
        Is this a win, loss, tie, or still in play for the X player?

        In progress:
        >>> State("XOX").check_status()
        'play'

        Win down the left hand side
        >>> State("XO_XO_X").check_status()
        'win'

        Lose down the bottom
        >>> State("__XXX_OOO").check_status()
        'loss'

        Win diagnoal
        >>> State("XOO_XO__X").check_status()
        'win'

        Loss diagnoal
        >>> State("X_OXO_OX").check_status()
        'loss'
        """
        for r in self.rotations():
            if r[0] == ['X','X','X']:
                return "win"
            elif r[0] == ['O','O','O']:
                return "loss"
            elif r[0][0] == "X" and r[1][1] == "X" and r[2][2] == "X":
                return "win"
            elif r[0][0] == "O" and r[1][1] == "O" and r[2][2] == "O":
                return "loss"
        return "play"


def print_examples():
   print(State((0,1,2)))

   print(State((0,1,3,4,6)))

   print(State((0,6,2,7,5,8)))

   print(State((0,2,4,5,8)))

   print(State((0,2,3,4,7,6)))

def main():
    print_examples()

if __name__ == "__main__":
    main()
