from os.path import join
from typing import *

import os

from score import score

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(CURRENT_PATH, './data')
OUTPUT_PATH = os.path.join(CURRENT_PATH, './output')

def read_data_from_file(file_path: str) -> Tuple[List[List[int]], List[int], Tuple[int]]:
  """Read data from file.

  Args:
    file_path: 文件绝对路径

  Returns:
    pizzas: 原料编码后的披萨
    cout_ings: 各个原料数量
    teams: 各个小队数量
  """
  f = open(file_path, 'r')
  raw_lines = f.readlines()
  _, t2, t3, t4 = list(map(int, raw_lines[0].split(' ')))
  pizzas = [line.strip().split(' ')[1:] for line in raw_lines[1:]]
  f.close()

  encode_ings = {}
  for p in pizzas:
    for ing in p:
      if ing not in encode_ings:
        encode_ings[ing] = len(encode_ings)

  cout_ings = [0] * len(encode_ings)
  pizzas = [[encode_ings[ing] for ing in p] for p in pizzas]

  # 计算每种原料数量
  for p in pizzas:
    for ing in p:
      cout_ings[ing] += 1

  return pizzas, cout_ings, (t2, t3, t4)

def write_solution(solutions):
  """Write solution to output."""
  pass

def solve(pizzas: List[int], cout_ings: List[int], teams: Tuple[int], w1: float = 0.5, w2: float = 0.5):
  """求解函数"""
  total_ings = sum(cout_ings) # 原料总数

  # 为每种 pizza 计算贪心稀有度量
  pizza_info = []
  max_freq, max_count = 0, 0
  for p in pizzas:
    total_freq = sum(cout_ings[ing] / total_ings for ing in p) # 每种原料的稀有度之和
    max_freq = max(max_freq, total_freq)
    max_count = max(max_count, len(p))
    pizza_info.append([total_freq, len(p), 0, 0]) # 稀有度，原料总数

  # 归一化原料频次
  for i in range(len(pizza_info)):
    pizza_info[i][0] /= max_freq
    pizza_info[i][1] /= max_count
    pizza_info[i][2] = i # 保存原始序列号
    pizza_info[i][3] = w1 * pizza_info[i][0] + w2 * pizza_info[i][1]

  # 贪心地排序并求解
  pizza_info_sorted = sorted(pizza_info, key= lambda x: x[-1])

  team_solution = {}
  pi = 0
  for ti, t in enumerate(teams):
    team_solution[ti] = []
    for i in range(t):
      if len(pizzas) - pi < ti + 2: break # 当披萨不够时，停止抽取
      pizza = [pizza_info_sorted[pi + j][2] for j in range(ti + 2)] # 从队列中选取 ti + 2 个披萨
      team_solution[ti].append(pizza)
      pi += ti + 2

  total_score = 0
  for ti in team_solution:
    s = score(team_solution[ti], pizzas)
    total_score += s
    # print(ti + 2, s)
  return total_score

def get_files():
  """Get all input files."""
  return [os.path.join(DATA_PATH, fp) for fp in os.listdir(DATA_PATH)]

def search_params(search_file_index: int = 0):
  """Search Params."""
  files = get_files()
  test_file = files[search_file_index]
  pizzas, cout_ings, teams = read_data_from_file(test_file)

  R = 5
  max_score = 0
  res = None
  for w1 in range(-R, R):
    for w2 in range(-R, R):
      if w1 == 0 and w2 == 0: continue
      pw1 = w1 / R
      pw2 = w2 / R
      s = solve(pizzas, cout_ings, teams, pw1, pw2)
      if s > max_score:
        max_score = s
        res = (pw1, pw2, s)
  print(res)
  return res

if __name__ == '__main__':
  search_params()

  total_score = 0
  for f in get_files():
    s = solve(*read_data_from_file(f), 0, -1)
    total_score += s
    print(os.path.basename(f), s)
  print('total', total_score)