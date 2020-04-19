def read_ints():
  return list(map(int, input().split(' ')))

def solve():
  t = int(input())
  for case in range(1, t + 1):
    w, h, l, u, r, d = read_ints()
    dp = [[0 for i in range(h + 1)] for j in range(w + 1)]
    for x in range(w, 0, -1):
      for y in range(h, 0, -1):
        if x == w and y == h:
          dp[x][y] = 1
          continue
        if l <= x and x <= r and u <= y and y <= d: continue
        if x == w:
          dp[x][y] = dp[x][y + 1]
        elif y == h:
          dp[x][y] = dp[x + 1][y]
        else:
          dp[x][y] = (dp[x + 1][y] + dp[x][y + 1]) / 2

    print('Case #%d: %f' % (case, dp[1][1]))

if __name__ == '__main__':
  solve()

'''
4
3 3 2 2 2 2
5 3 1 2 4 2
1 10 1 3 1 5
6 4 1 3 3 4
'''