import numpy as np
from itertools import product

class GameRunner:
  def __init__(self):
    '''A GameRunner simulates conway's game of life on a two-dimension world.

    Example:
      runner = GameRunner()
      # random init
      runner.random_init(10, 10)
      # custom init
      runner.set_world(custom_matrix)
      # simulate for one step
      runner.step()
      # 10 steps
      runner.steps(10)
      # fetch world matrix
      mat = runner.get_world()
    '''
    self.t = 0
    self.world = None # type: np.ndarray


  def step(self):
    '''Simulates for the next time step.
    '''
    self.t += 1
    temp_world = self.world.copy() # old state
    rows, cols = self.world.shape

    for row, col in product(range(rows), range(cols)):
      # count the number of surrounding live cells
      count_live = 0
      for adj_row, adj_col in product([row - 1, row, row + 1], [col - 1, col, col + 1]):
        adj_row = (adj_row + rows) % rows
        adj_col = (adj_col + cols) % cols
        count_live += temp_world[adj_row, adj_col]

      if temp_world[row, col]:
        # live -> death
        if count_live < 2 or count_live > 3:
          self.world[row, col] = 0
      else:
        # death -> live
        if count_live == 3:
          self.world[row, col] = 1


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


  def random_init(self, rows: int, cols: int, p: float = 0.5):
    '''Initalize a rows * cols world randomly with a probability of p.

    Args:
      rows: rows of the world
      cols: cols of the world
      p: live probability for each cell
    '''
    assert rows > 0 and cols > 0, "Zero dimension is not allowed."
    assert p >= 0 and p <= 1, "Probability should be in [0, 1]."
    self.world = np.random.rand(rows, cols)
    self.world[self.world > p] = 1
    self.world[self.world <= p] = 0