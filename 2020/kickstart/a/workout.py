import math

def read_ints():
  return list(map(int, input().split(' ')))

def solve():
  t = int(input())
  for case in range(1, t + 1):
    n, k = read_ints()
    session = read_ints()
    diff = []
    for i in range(n - 1):
      d = session[i + 1] - session[i]
      diff.append(d)
    diff.sort(reverse=True)
    l, r = 1, diff[0]
    while l < r:
      m = (l + r) >> 1
      csum = sum([math.ceil(x / m) - 1 for x in diff])
      if csum <= k: r = m
      else: l = m + 1
    print('Case #{}: {}'.format(case, l))

if __name__ == "__main__":
  solve()