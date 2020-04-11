import math
from itertools import product

def read_ints():
  return list(map(int, input().split(' ')))

def solve():
  t = int(input())
  for case in range(1, t + 1):
    m, l = read_ints()
    mat = []
    for i in range(m):
      mat.append(read_ints())
    x, y = read_ints()
    visited = [[False for i in range(m)] for j in range(m)]
    q = [(x, y)]
    while q:
      nextq = []
      oldl = l
      for r, c in q:
        visited[r][c] = True
        if d(x, y, r, c) > l: # 砍不到的点放回队列
          nextq.append((r, c))
        else: # 能砍到的点加到刀的长度上
          l += mat[r][c]
          mat[r][c] = 0
          # 扩展点
          for dr, dc in product([-1, 0, 1], [-1, 0, 1]):
            nr, nc = r + dr, c + dc
            if nr >= 0 and nr < m and nc >= 0 and nc < m and not visited[nr][nc]:
              nextq.append((nr, nc))
      if len(nextq) == len(q) and l == oldl: break
      q = nextq
    print(l)

def d(x1, y1, x2, y2):
  return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

if __name__ == '__main__':
  solve()

'''
3
4 1
0 0 0 0
0 1 0 0
0 0 1 0
0 0 0 1
1 2
10 3
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 2 0 0 0
0 0 0 0 0 0 0 0 0 2
0 0 0 1 0 0 0 0 0 1
0 0 0 1 0 0 2 0 2 0
8 8
10 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 1 0 0 0 0
0 0 0 1 2 0 2 0 0 0
0 0 0 0 2 1 2 0 2 0
0 0 2 0 0 0 0 0 2 0
0 0 0 0 0 0 0 2 0 0
0 0 0 1 0 0 0 0 0 0
2 5
'''