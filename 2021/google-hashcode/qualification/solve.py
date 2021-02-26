from os.path import samefile
from typing import *
import os, math, random

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(CURRENT_PATH, './data')
OUTPUT_PATH = os.path.join(CURRENT_PATH, './output')

def get_files():
  """获取所有的输入文件"""
  return [os.path.join(DATA_PATH, fp) for fp in os.listdir(DATA_PATH)]

def read_file(fp: str) -> Tuple[Tuple[int], Tuple[List[Tuple[str, int, int, int]], Dict[str, int], Set[Set[int]], List[List[int]]]]:
  """从文件中读取数据

  Args:
    fp: 文件路径

  Returns:
    (D, I, S, V, F): 首行信息
    (street_info, name_to_int, has_street): 街道信息
    cars: 车辆信息
    problem: 问题名称
  """
  problem = os.path.basename(fp)
  f = open(fp, 'r')
  lines = f.read().split('\n')
  f.close()

  D, I, S, V, F = list(map(int, lines[0].split(' ')))

  # 读取街道
  street_info = [None] * S # 用于存储街道信息
  name_to_int = {} # 街道名称到 int 的编码
  has_street: Set[Set[int]] = set() # 用于判断某两个节点之间是否存在街道
  for i in range(S):
    begin, end, name, length = lines[i + 1].split(' ')
    begin, end, length = int(begin), int(end), int(length)
    name_to_int[name] = i # 编码名称
    has_street.add((begin, end)) # 更新邻接表
    street_info[i] = (name, length, begin, end) # 存储街道信息

  # 读取车辆
  cars = [None] * V
  for i in range(V):
    car_path = lines[S + 1 + i].split(' ')
    cars[i] = [name_to_int[name] for name in car_path[1:]]

  return (D, I, S, V, F), (street_info, name_to_int, has_street), cars, problem

def simulate():
  """模拟车辆运行情况"""
  pass

def solve_d(base_info, street_infos, cars, problem: str):
  """求解 D"""
  print(problem)
  dur, inter_count, street_count, car_count, bonus = base_info
  street_info, name_to_int, has_street = street_infos

  print(cars[0])
  # 贪心地规划对应地车辆
  inter_flags = [-1] * inter_count
  for car in cars:
    # 确认是否能到达
    ok = True
    for street in car:
      to_inter = street_info[street][-1]
      ok = ok and inter_flags[to_inter] < 0
    if not ok: continue
    # 否则贪心处理车辆
    for street in car:
      to_inter = street_info[street][-1]
      inter_flags[to_inter] = street

  solution = []
  for i in range(inter_count):
    if inter_flags[i] < 0: continue
    solution.append((i, [(inter_flags[i], dur)]))
  print(len(solution))

  write_file(solution, problem, street_info)

def solve(base_info, street_infos, cars, problem: str):
  """求解器"""
  print(problem)
  dur, inter_count, street_count, car_count, bonus = base_info
  street_info, name_to_int, has_street = street_infos

  # 根据车辆路径，更新路口经过车辆的统计信息
  inter_info = [[[0] * dur, {}, 0] for i in range(inter_count)] # [count] * dur, group_count[st], total_cars
  total_cars = 0
  max_score = bonus * car_count
  total_length = 0
  for car in cars:
    t = 0 # 路径时间
    total_time = sum(street_info[street][1] for street in car)
    if (total_time > dur): continue
    total_length += len(car)
    total_cars += 1
    for street in car:
      to_inter = street_info[street][-1] # 当前路径的结束路口
      inter = inter_info[to_inter] # 取到路口信息
      inter[0][t] += 1 # 累加路口经过车辆数
      if street not in inter[1]: inter[1][street] = 0
      inter[1][street] += 1 # 按驶入车道统计车辆频次
      inter[2] += 1 # 更新经过该路口的车辆总数
      t += street_info[street][1] # 累加车辆运行时间
    max_score += max(0, dur - t)
  print('总车辆：', total_cars)
  print('理论得分：', max_score)
  print('平均剩余耗时：', (max_score - total_cars * bonus) / total_cars)
  print('平均路径长度：', total_length / total_cars)

  # 统计平均每个路口经过的车辆数
  cars_per_inter = [inter[-1] for inter in inter_info]
  streets_per_inter = [len(inter[1]) for inter in inter_info]
  avg_cars = sum(cars_per_inter) / len(inter_info)
  print('每个路口车辆通勤（平均，最大，最小）：', avg_cars, max(cars_per_inter), min(cars_per_inter))
  print('平均每个路口街道数', sum(streets_per_inter) / len(inter_info))

  solution = []
  # 开始调度
  for i in range(inter_count):
    count_t = inter_info[0]
    street_count: Dict = inter_info[i][1]
    total_cars = inter_info[i][2]
    if total_cars == 0: continue # 没车来，就跳过该路口
    T = dur # 调度周期默认等于总长度

    # 只调度最多的四个街道
    streets_sorted = list(street_count.items())
    streets_sorted.sort(key=lambda x: x[1], reverse=True)
    # print(streets_sorted[:int(len(streets_sorted) * 0.8)])
    street_count = {}
    total_cars = 0
    for street, st in streets_sorted: # 只调度前四个
      street_count[street] = st
      total_cars += st
    inter_info[i][1] = street_count
    inter_info[i][2] = total_cars

    if len(street_count) > 1: # 限制基础调度周期
      T = min(max(len(street_count), total_cars // len(street_count)), dur)
    streets = []
    remain_time = dur # 剩余调度时间
    for street in street_count:
      st = math.ceil(street_count[street] / total_cars * T)
      st = min(max(1, st), remain_time) # 调度时间不能超过总时长
      if problem.endswith('d.txt'): st = 1
      streets.append((street, st)) # 街道名称，调度时长
      remain_time -= st # 减去已经调度时长
    solution.append((i, streets))

  # 写入答案
  write_file(solution, problem, street_info)
  return max_score

def write_file(solution: List[Tuple[int, List[Tuple[int, int]]]], problem: str, street_info: List[Tuple[str, int, int, int]]):
  """写入文件"""
  with open(os.path.join(OUTPUT_PATH, problem), 'w') as f:
    f.write('{}\n'.format(len(solution)))
    for (inter, streets) in solution:
      f.write('{}\n{}\n'.format(inter, len(streets)))
      for (street, st) in streets:
        f.write('{} {}\n'.format(street_info[street][0], st))
  print('done\n')

if __name__ == '__main__':
  files = get_files()
  max_s = 0
  for f in files:
    data = read_file(f)
    max_s += solve(*data)
  print('\n\n理论最高总分：', max_s)