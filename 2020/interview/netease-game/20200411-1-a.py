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
    mat[x][y] = l
    oldl = l - 1
    while l > oldl:
      oldl, l = l, 0
      for r in range(m):
        for c in range(m):
          if d(r, c, x, y) <= oldl:
            l += mat[r][c]
    print(l)

def d(x1, y1, x2, y2):
  return ((x1 - x2) * (x1 - x2) + (y1 - y2) *  (y1 - y2)) ** 0.5

if __name__ == '__main__':
  solve()