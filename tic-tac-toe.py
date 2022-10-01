#!/bin/python
from collections import defaultdict

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

        >>> State("X").next
        'O'

        >>> State().next
        'X'

        """
        if len(s) > 9:
            raise ValueError("too many moves")
        if set(s) - {'X', 'O', '_'} != set():
            raise ValueError("invalid characters")
        x_moves = s.count('X')
        o_moves = s.count('O')
        move_differences = x_moves - o_moves
        if move_differences > 1 or move_differences < 0:
            raise ValueError("illegal board state")
        self.s = dict(enumerate(s.ljust(9,"_")))
        self.str = State.to_str(self.s)
        self.board = self.to_board()
        self.victory = self.check_status()
        self.next = 'X' if x_moves == o_moves else 'O'
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

    @staticmethod
    def to_str(d: dict):
        """
        >>> State.to_str(State("X_O").s)
        'X_O______'
        """
        return "".join([d[i] for i in range(9)])

    def children(self):
        """
        >>> for child in State("X").children(): print(child)
        XO_
        ___
        ___
        <BLANKLINE>
        X_O
        ___
        ___
        <BLANKLINE>
        X__
        O__
        ___
        <BLANKLINE>
        X__
        _O_
        ___
        <BLANKLINE>
        X__
        __O
        ___
        <BLANKLINE>
        X__
        ___
        O__
        <BLANKLINE>
        X__
        ___
        _O_
        <BLANKLINE>
        X__
        ___
        __O
        <BLANKLINE>

        >>> for child in State("XXXOO_O").children(): print(child)
        """
        if self.victory != "play":
            return()

        for i in range(9):
            if self.s[i] == '_':
                ss = self.s.copy()
                ss[i] = self.next
                yield State(State.to_str(ss))

    def __str__(self):
        """
        >>> print(State())
        ___
        ___
        ___
        <BLANKLINE>
        >>> print(State("__X"))
        __X
        ___
        ___
        <BLANKLINE>
        >>> print(State("_OX_OXO_X"))
        _OX
        _OX
        O_X
        <BLANKLINE>
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

        Tie
        >>> State("XOXXXOOXO").check_status()
        'tie'
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
        if self.str.count('_') == 0:
            return 'tie'
        else:
            return "play"


def make_tree():
    nodes = {"": State()}
    children = defaultdict(list)
    leaves = set()

    visited = set()
    to_visit = nodes.keys() - visited
    while len(to_visit) > 0:
        node_key = to_visit.pop()
        node = nodes[node_key]
        visited.add(node_key)
        i = 0
        for child in node.children():
            s = child.str
            children[node_key].append(s)
            nodes[s] = child
            i+=1
        if i == 0: # no children; win/loss/tie node
            leaves.add(node_key)
        to_visit = nodes.keys() - visited

    return({"nodes": nodes,
            "children": children,
            "leaves": leaves})

def main():
    res = make_tree()
    for i, item in enumerate(res['children'].items()):
        print(item)
        if i == 10:
            break
    c = defaultdict(int)
    for i, item in enumerate(res['leaves']):
        c[res['nodes'][item].victory] += 1
    print(c)

if __name__ == "__main__":
    main()
