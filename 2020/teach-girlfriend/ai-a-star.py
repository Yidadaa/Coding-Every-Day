"""An example solution for my girlfriend."""

from __future__ import annotations
import random
from itertools import permutations, product
from functools import reduce, lru_cache
from typing import Callable, List, Dict, Tuple
from queue import PriorityQueue
import time

PuzzleType = List[List[int]]

class EFPuzzleState():
  """Define state for eight figure puzzle problem."""

  def __init__(self, state: PuzzleType, g: int = 0, h: int = 0, parent: int = -1) -> None:
    """Define state with g value and h value.

    Args:
      state: 3 * 3 matrix denotes state
      g: g value for the state
      h: h value for the state
      parent: parent state index in node list
    """
    self.state = state
    self.g, self.h = g, h
    self.parent = parent
    self.rows, self.cols = len(state), len(state[0])
    self.__hash_val = None

  @staticmethod
  def hash(state: PuzzleType):
    """Hash function for PuzzleType."""
    hash_value = 0
    w, h = len(state), len(state[0])
    for i in range(w * h):
      hash_value = hash_value * 10 + state[i // w][i % w]
    return hash_value

  @lru_cache()
  def zero_index(self) -> Tuple[int, int]:
    """Find index of zero in the state matrix."""
    for r, c in product(range(self.rows), range(self.cols)):
      if self.state[r][c] == 0: return r, c

  @lru_cache()
  def f(self) -> int:
    """F value for the state."""
    return self.g + self.h

  @lru_cache()
  def adj_states(self) -> List[PuzzleType]:
    """Adjacent states of the state."""
    adj_list = [] # type: List[PuzzleType]
    zr, zc = self.zero_index()
    for dr, dc in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
      r, c = zr + dr, zc + dc
      if r >= self.rows or r < 0 or c >= self.cols or c < 0: continue
      self.state[r][c], self.state[zr][zc] = self.state[zr][zc], self.state[r][c]
      adj_list.append([line.copy() for line in self.state])
      self.state[r][c], self.state[zr][zc] = self.state[zr][zc], self.state[r][c]
    return adj_list

  def __lt__(self, other: EFPuzzleState) -> bool:
    """Override less behavior of the state."""
    return self.f() < other.f()

  def __hash__(self) -> int:
    """Hash function of the state."""
    if not self.__hash_val:
      self.__hash_val = self.hash(self.state)
    return self.__hash_val

  def __str__(self) -> str:
    """Print-friendly string."""
    return '\n'.join(' '.join([str(x) for x in line]) for line in self.state)

class EightFigurePuzzle():
  """Solve eight figure puzzle problem with a star."""

  def __init__(self, puzzle: PuzzleType = None, target: PuzzleType = None, \
      h_function: Callable[[PuzzleType, PuzzleType], int] = None) -> None:
    """Init with puzzle, target and h(x).

    Args:
      puzzle: initial state, default: self.random_state()
      target: target state, default: self.random_state()
      h_function: h(x) function, default: self.default_h_function
    """
    self.N, self.W = 9, 3
    self.MAX_STATE_COUNT = reduce(lambda l, c: l * c, range(1, self.N + 1))
    self.puzzle = self.random_state() if puzzle is None else puzzle
    self.target = self.random_state() if target is None else target
    self.h_function = self.default_h_function if h_function is None else h_function
    self.close_list = {} # type: Dict[int, EFPuzzleState]

  def solve(self):
    """Solve the prolem."""
    target_hash = EFPuzzleState.hash(self.target)
    dq = PriorityQueue() # type: PriorityQueue[EFPuzzleState]
    dq.put(EFPuzzleState(self.puzzle, 0, self.h_function(self.puzzle, self.target), -1))
    while not dq.empty():
      state = dq.get()
      if state.__hash__() in self.close_list: continue
      self.close_list[state.__hash__()] = state
      if state.__hash__() == target_hash: break
      for adj_state in state.adj_states():
        adj_state = EFPuzzleState(adj_state, state.g + 1, self.h_function(adj_state, self.target), state.__hash__())
        dq.put(adj_state)

  def show_output(self):
    """Print result of the puzzle. """
    puzzle_state = EFPuzzleState(self.puzzle)
    target_state = EFPuzzleState(self.target)
    target_hash = target_state.__hash__()

    print('Init state:\n' + str(puzzle_state) + '\n')
    print('Target state:\n' + str(target_state) + '\n')

    # check if no solution
    if target_hash not in self.close_list:
      print('No Solution.')

    # print path
    path = [] # type: List[EFPuzzleState]
    while target_hash in self.close_list:
      path.append(self.close_list[target_hash])
      target_hash = self.close_list[target_hash].parent
    print('Path:')
    while path:
      print(str(path.pop()) + '\n')

  @staticmethod
  def default_h_function(state: PuzzleType, target: PuzzleType) -> int:
    """Define default h(x) if there is no h_function defined by user."""
    rows, cols = len(state), len(state[0])
    return sum(int(state[r][c] != target[r][c])
      for r, c in product(range(rows), range(cols)))

  def random_state(self) -> list:
    """Get random state as initial puzzle."""
    puzzle_generator = permutations(range(self.N))

    # generate puzzle randomly
    times = random.randint(0, self.MAX_STATE_COUNT)
    for _ in range(times): next(puzzle_generator)
    puzzle = next(puzzle_generator)
    return self.reshape(puzzle)

  def reshape(self, one_dimension_state: List[int]) -> PuzzleType:
    """Reshape puzzle to 3 * 3 matrix"""
    reshaped_puzzle = [[0] * self.W for _ in range(self.W)]
    for r, c in product(range(self.W), range(self.W)):
      reshaped_puzzle[r][c] = one_dimension_state[r * self.W + c]
    return reshaped_puzzle

if __name__ == "__main__":
  puzzle = [
    [1, 3, 0],
    [8, 2, 4],
    [7, 6, 5]
  ]
  target = [
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5]
  ]

  time_point = time.time()
  bfs_solver = EightFigurePuzzle(puzzle=puzzle, target=target, h_function=lambda _, __: 0) # type: ignore
  bfs_solver.solve()
  bfs_solver.show_output()
  print('BFS: %.4f' % (time.time() - time_point))

  time_point = time.time()
  astar_solver = EightFigurePuzzle(puzzle=bfs_solver.puzzle, target=bfs_solver.target)
  astar_solver.solve()
  astar_solver.show_output()
  print('A star: %.4f' % (time.time() - time_point))