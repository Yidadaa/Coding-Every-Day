t = int(input())

for i in range(t):
  s = input()
  cnt = 0
  for c in s:
    cnt += 1 - int(c)
  si = 0
  while si < len(s) and s[si] == '0': si += 1
  cnt -= si
  if si != len(s):
    ei = len(s) - 1
    while ei >= 0 and s[ei] == '0': ei -= 1
    cnt -= len(s) - ei - 1
  print(cnt)