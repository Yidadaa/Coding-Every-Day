import numpy as np
from itertools import product
from time import time

class GameRunner:
  def __init__(self):
    '''A GameRunner simulates conway's game of life on a two-dimension world.

    Example:
      runner = GameRunner()
      runner.random_init(10, 10)
      runner.set_world(custom_matrix)
      runner.step()
      runner.steps(10)
      mat = runner.get_world()
    '''
    self.t = 0
    self.world = None # type: np.ndarray
    self.live_count = 0
    self.dead_count = 0

  def step(self):
    '''Simulates for the next time step.
    '''
    self.t += 1
    rows, cols = self.world.shape

    count_live = np.zeros((rows, cols))
    for dr, dc in product([-1, 0, 1], [-1, 0, 1]):
      count_live += np.roll(self.world, (dr, dc), axis=(0, 1))
    count_live -= self.world

    live_mask = self.world > 0
    dead_mask = self.world < 1
    eq_three_mask = count_live == 3
    le_two_mask = count_live < 2
    lg_three_mask = count_live > 3
    to_live_mask = le_two_mask + lg_three_mask
    to_live_mask = to_live_mask > 0
    self.world[live_mask * to_live_mask] = 0
    self.world[dead_mask * eq_three_mask] = 1
    self.update_count()


  def update_count(self):
    '''Counts live and dead cells.
    '''
    self.live_count = int(np.sum(self.world))
    self.dead_count = self.world.size - self.live_count


  def steps(self, n: int):
    '''Simulates for next n steps.

    Args:
      n: steps to simulate
    '''
    for i in range(n):
      self.step()


  def get_world(self) -> np.ndarray:
    '''Return the world matrix.
    '''
    return self.world


  def set_world(self, new_world: np.ndarray):
    '''Set a new world matrix.

    Args:
      new_world: a np.array that describes the new world
    '''
    assert len(new_world.shape) == 2, "Wrong dimension for the new world."
    self.world = new_world
    self.t = 0
    self.update_count()


  def random_init(self, rows: int, cols: int, p: float = 0.5):
    '''Initalize a rows * cols world randomly with a probability of p.

    Args:
      rows: rows of the world
      cols: cols of the world
      p: live probability for each cell
    '''
    assert rows > 0 and cols > 0, "Zero dimension is not allowed."
    assert p >= 0 and p <= 1, "Probability should be in [0, 1]."
    random_world = np.random.rand(rows, cols)
    random_world[random_world > p] = 0
    random_world[random_world > 0] = 1
    self.set_world(random_world)