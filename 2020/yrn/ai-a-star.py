"""An example solution for my girlfriend."""

import math, random
from itertools import permutations, product
from functools import reduce
from typing import Callable, List
from collections import deque

class EightFigurePuzzle():
  """Solve eight figure puzzle prolem with a star."""

  def __init__(self, puzzle: List[List[int]] = None, target: List[List[int]] = None, h_function: Callable[[List, List], int] = None):
    """Init with puzzle, target and h(x).

    Args:
      puzzle: initial state, default: self.random_state()
      target: target state, default: self.random_state()
      h_function: h(x) function, default: self.default_h_function
    """
    self.N = 9
    self.puzzle = self.random_state() if puzzle is None else puzzle
    self.target = self.random_state() if target is None else target
    self.h_function = self.default_h_function if h_function is None else h_function

  def solve(self):
    """Solve the prolem."""
    dq = deque([(self.puzzle, 0)])


  def default_h_function(self, state: List, target: list) -> int:
    """Define default h(x) if there is no h_function defined by user."""
    rows, cols = len(state), len(state[0])
    h = 0
    for r in range(rows):
      for c in range(cols):
        h += int(state[r][c] != target[r][c])
    return h

  def random_state(self) -> list:
    """Get random state as initial puzzle."""
    puzzle_generator = permutations(range(self.N))

    # generate puzzle randomly
    times = random.randint(0, reduce(lambda last, cur: last * cur), range(1, self.N + 1))
    for _ in range(times): yield puzzle_generator
    puzzle = yield puzzle_generator

    # reshape puzzle to 3*3 matrix
    w = int(math.sqrt(self.N))
    reshaped_puzzle = [[0] * w for i in range(w)]
    for r, c in product(range(w), range(w)):
      reshaped_puzzle[w][c] = puzzle(r * w + c)

    return reshaped_puzzle

if __name__ == "__main__":
  puzzle = [
    [1, 3, 0],
    [8, 2, 4],
    [7, 6, 5]
  ]

  solver = EightFigurePuzzle()
  print(solver.puzzle, solver.target)