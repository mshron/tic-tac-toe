#!/bin/python

class State:
    def __init__(self, id: tuple = None):
        """
        id is a tuple of indexes, in order of moves.  We assume X always goes first.

        Mapping from index to spot:
        0 1 2
        3 4 5
        6 7 8

        So (0, 1) would be

        X O _
        _ _ _
        _ _ _

        >>> a = State((0,0))
        Traceback (most recent call last):
        ...
        ValueError: all moves must be unique
        """
        if len(set(id)) != len(id): # check for duplicates
            raise ValueError("all moves must be unique")
        self.id = id
        self.victory = False
        self.leads_to_win = 0
        self.leads_to_tie = 0
        self.leads_to_loss = 0

    def __str__(self):
        out = [["_" for j in range(3)] for i in range(3)]
        turn = "X"
        for n in self.id:
           i = n % 3
           j = n // 3
           out[j][i] = turn
           if turn == "X":
               turn = "O"
           else:
               turn = "X"
        return("\n".join(["".join(row) for row in out]) + "\n")

    def as_ternary(self):
        out = [[0 for j in range(3)] for i in range(3)]
        turn = 1
        for n in self.id:
           i = n % 3
           j = n // 3
           out[j][i] = turn
           turn *= -1
        return out

    def rotations(self):
        """
        Return an iterator of the four rotational symmetries of the board
        """

    def check_status(self):
        """
        Is this a win, loss, tie, or still in play for the X player?

        In progress:
        >>> State((0,1,2)).check_status()
        "play"

        Win down the left hand side
        >>> State((0,1,3,4,6)).check_status()
        "win"

        Lose down the bottom
        >>> State((0,6,2,7,5,8)).check_status()
        "loss"

        Win diagnoal
        >>> State((0,2,4,5,8)).check_status()
        "win"

        Loss diagnoal
        >>> State((0,2,3,4,7,6))
        "loss"
        """




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
