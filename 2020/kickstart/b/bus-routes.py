import math

def read_ints():
  return list(map(int, input().split(' ')))

def solve():
  t = int(input())
  for case in range(1, t + 1):
    n, d = read_ints()
    routes = read_ints()
    def check(day):
      for r in routes:
        the_day = math.ceil(day / r) * r
        if the_day > d: return False
        day = the_day
      return True
    l, r = 1, d
    while l < r:
      m = (l + r) >> 1
      if not check(m): r = m
      else: l = m + 1
    if not check(l): l -= 1
    print('Case #{}: {}'.format(case, l))

if __name__ == '__main__':
  solve()

'''
3
3 10
3 7 2
4 100
11 10 5 50
1 1
1
'''