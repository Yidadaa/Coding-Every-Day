import time

off_line = True
inputs = '''3
2 3
1 2
3 3
2 5
2 2
12 30
12 12
2 3 2 1 2 3 2 1 2 3 1 2
1 2 3 4 1 2 3 4 1 2 1 2
'''.split('\n')
i_index = 0

def get_input():
  global i_index
  if off_line:
    i_index += 1
    return inputs[i_index - 1]
  else:
    return input()

def read_int()->list:
  s = get_input()
  return list(map(int, s.split(' ')))


def check(num:int, n:int, h:int, a:list, b:list)->bool:
  count_a, count_b = 0, 0
  thary, tmp = '', num
  for index in range(n - 1, -1, -1):
    state = (num % 3) + 1
    has_a = state & 1
    has_b = (state >> 1) & 1
    if has_a + has_b < 1: break
    num //= 3
    count_a += has_a * a[index]
    count_b += has_b * b[index]
    if count_a >= h and count_b >= h: break
  cond = count_a >= h and count_b >= h
  return cond

def solve(case:int):
  n, h = read_int()
  a = read_int()
  b = read_int()

  ret = 0

  if sum(a) >= h and sum(b) >= h:
    # min and max
    min_n = 1
    max_n = 3 ** n

    i = min_n - 1
    while i < max_n:
      i += 1
      if check(i, n, h, a, b): ret += 1

  print('Case #{}: {}'.format(case + 1, ret))

if __name__ == "__main__":
  t = read_int()[0]
  for i in range(t):
    solve(i)