t = int(input())

for i in range(t):
  n, g, b = map(int, input().split(' '))
  hn = (n + n % 2) // 2
  gn = hn % g
  bn = (hn // g + int(gn > 0) - 1) * (g + b)
  print(gn + bn)