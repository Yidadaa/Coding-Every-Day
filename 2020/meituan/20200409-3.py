def read_ints():
  return list(map(int, input().split(' ')))

def solve():
  n, k = read_ints()
  l, r = 0, n
  while l < r:
    m = (l + r) >> 1
    if check(m, n, k): r = m
    else: l = m + 1
  print(l)

def check(x, n, k):
  while x > 0:
    n -= x
    x //= k
  return n <= 0

if __name__ == '__main__':
  solve()
