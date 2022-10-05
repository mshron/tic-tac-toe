#!/bin/python
from collections import defaultdict, OrderedDict

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

        >>> State("X").player
        'O'

        >>> State().player
        'X'

        >>> State().depth
        0

        >>> State('X').depth
        1

        >>> State('XXOXXOOOX').depth
        9

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
        self.depth = 9 - self.str.count('_')
        self.board = self.to_board()
        self.status = self.check_status()
        self.player = 'X' if x_moves == o_moves else 'O'
        self.set_default_value()

    def set_default_value(self):
        if self.status == 'tie':
            self.value = 0
        elif self.status == 'win':
            self.value = 10 - self.depth
        elif self.status == 'loss':
            self.value = self.depth - 10
        elif self.player == 'X':
            self.value = -999
        else:
            self.value = 999

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

    def make_children(self):
        """
        >>> for child in State("X").make_children(): print(child)
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

        This should be empty, since it's a leaf node (X wins)
        >>> for child in State("XXXOO_O").make_children(): print(child)
        """
        # leaf node
        if self.status != "play":
            return()

        for i in range(9):
            if self.s[i] == '_':
                ss = self.s.copy()
                ss[i] = self.player
                yield (i, State(State.to_str(ss)))

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
    """
    Create the tree of all games

    Returns `nodes` which has all of the node data, plus `leaves`
    which covers all of the final leaves, `children` which is a tuple
    of (move, state), and `parents` which is self-explanatory.

    Everything keys off of the string.
    """
    nodes = {"_________": State()}
    parents = defaultdict(list)
    children = defaultdict(list)
    leaves = set()

    visited = set()
    to_visit = nodes.keys() - visited
    while len(to_visit) > 0:
        node_key = to_visit.pop()
        node = nodes[node_key]
        visited.add(node_key)
        i = 0
        for move, child in node.make_children():
            s = child.str
            parents[s].append(node_key)
            children[node_key].append((move, s))
            nodes[s] = child
            i += 1
        if i == 0: # no children; win/loss/tie node
            leaves.add(node_key)
        to_visit = nodes.keys() - visited

    return({"nodes": nodes,
            "parents": parents,
            "children": children,
            "leaves": leaves})
def minimax(nodes: dict, children: dict, leaves: set, parents: dict):
    """
    Start from the end, work backwards to recusively identify the right moves for each player

    See https://www.neverstopbuilding.com/blog/minimax for good discussion of minimax strategy,
    and https://www.youtube.com/watch?v=STjW3eH0Cik for a good MIT OCW video on it.

    """
    to_visit = OrderedDict()
    for leaf in leaves:
        for p in parents[leaf]:
            to_visit[p] = None

    while len(to_visit) > 0:
        node_key = to_visit.popitem(last=False)[0] # FIFO
        node = nodes[node_key]
        if node.player == 'X':
            node.value = max([nodes[c[1]].value for c in children[node_key]])
        else: # minimize
            node.value = min([nodes[c[1]].value for c in children[node_key]])

        for p in parents[node_key]:
            to_visit[p] = None

def make_htmls(nodes: dict, children: dict):
    for node_str, node in nodes.items():
        cs = dict(children.get(node_str, []))
        out = "<html><body><style>body{font-family: monospace;}</style>\n"
        for i in range(9):
            n = node.s[i]
            v = cs.get(i)
            if v == None:
                out += f'{n}|'
            else:
                out += f'<a href="{v}.html">_</a>|'
            if ((i+1) % 3 == 0):
                out = out[:-1] + "</br>\n"

        out += "</body></html>"
        with open(f'out/{node_str}.html', 'wt') as f:
            f.write(out)


def main():
    res = make_tree()
    nodes = res['nodes']
    parents = res['parents']
    children = res['children']
    leaves = res['leaves']

    minimax(nodes, children, leaves, parents)

    make_htmls(nodes, children)

if __name__ == "__main__":
    main()
