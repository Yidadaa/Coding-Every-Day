from typing import *

def score(s: List[List[int]], p: List[List[int]]) -> float:
  """Score of current solution.

  Args:
    s: 解的数组，例如：s = [[1, 2], [3, 4]]，s[0] = [1, 2]，表示一个二人小队，分到的披萨编号是 1 和 2，可以根据 pizzas[1] 和 pizzas[2] 取到披萨原料
    p: 披萨原料表，p[1] = [12, 23, 34] 表示编号为 1 的披萨的原料为 12, 23, 34

  Returns:
    score: 题目要求的分数
  """
  res = 0
  for pizzas in s:
    ingredients = set()
    for pizza in pizzas:
      ingredients.update(p[pizza])
    res += len(ingredients) ** 2
  return res

if __name__ == '__main__':
  s = [[1,2], [0, 2], [0, 1, 2]]
  p = {0: [0, 1, 2], 1: [0, 3], 2: [4, 5]}
  res = score(s, p)
  print('*' * 50)
  print('Total score is:', res)
  