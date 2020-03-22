'''
Python 真的垃圾，同样的代码疯狂 TLE。
'''

def read_ints():
  return list(map(int, input().split(' ')))

def solve():
  t = int(input())
  for case in range(1, t + 1):
    n, k, p = read_ints()
    dp = [[[0 for _ in range(k + 1)] for j in range(p + 1)] for i in range(n)]
    for i in range(n):
      stack = read_ints()
      s = 0
      for j in range(k + 1):
        if j > 0: s += stack[j - 1]
        if i == 0:
          if j < p + 1: dp[i][j][j] = s
          continue
        for tp in range(j, p + 1):
          m = max(dp[i - 1][tp - j])
          dp[i][tp][j] = m + s
    ret = max(dp[n - 1][p])
    print('Case #{}: {}'.format(case, ret))

if __name__ == "__main__":
  solve()

'''
3
3 10 1
12 43 54 23 54 21 12 32 12 5
2 3 554 23 52 11 1 3 222 50
2 3 554 23 52 11 1 3 222 50
2 4 5
10 10 100 30
80 50 10 50
3 2 3
80 80
15 50
20 10
'''