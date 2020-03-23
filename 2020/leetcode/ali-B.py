# xiaomai

def solve(t):
  m, n = len(t), len(t[0])
  MAX_STEPS = m * n + 1
  st, ed = None, None
  # 找到起点和终点
  for i in range(m):
    for j in range(n):
      if t[i][j] == 'S': st = (i, j)
      elif t[i][j] == 'E': ed = (i, j)
  flags = [[[MAX_STEPS, 5] for i in range(n)] for j in range(m)] # 是否遍历过，最小步数，飞行次数
  # BFS
  q = [(st[0], st[1], 5, 0)] # x, y, 可用飞行次数，耗时
  while q:
    x, y, fly, steps = q.pop()
    if steps < flags[x][y][0]:
      flags[x][y] = [steps, fly] # 更新最小步数
    if t[x][y] == 'E' or t[x][y] == '#': # 达到终点或者不能走
      continue
  
    # 否则继续走
    for nx, ny, nfly in [
      (x - 1, y, fly), (x + 1, y, fly),
      (x, y - 1, fly), (x, y + 1, fly),
      (m - 1 - x, n - 1 - y, fly - 1)
    ]:
      if nfly < 0: continue # 飞行次数用完了，不让飞
      if nx < 0 or nx >= m or ny < 0 or ny >= n: continue # 超出数组范围了，不让走
      if t[nx][ny] == '#': continue # 有障碍物，不让走
      if flags[nx][ny][0] < steps + 1: continue
      q.append((nx, ny, nfly, steps + 1))
  return -1 if flags[ed[0]][ed[1]][0] == MAX_STEPS else flags[ed[0]][ed[1]][0]

if __name__ == "__main__":
  t = [
    '#S...',
    'E#...',
    '#....',
    '.....'
  ]
  ret = solve(t)
  print(ret)