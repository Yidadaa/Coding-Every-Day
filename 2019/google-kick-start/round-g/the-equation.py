off_line = True
inputs = '''4
3 27
8 2 5
4 45
30 0 4 11
1 0
100
6 2
5 5 1 5 1 0
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

def solve(case:int):
  n, m = read_int()
  array = read_int()

  max_k = max(m, max(array))
  max_k = 1 << (len(bin(max_k)) - 2)
  ret_k = -1

  for k in range(max_k + 1):
    s = m
    for a in array:
      if s < 0:
        break
      s -= a ^ k
    if s < 0: continue
    else:
      ret_k = k

  print('Case #{}: {}'.format(case + 1, ret_k))

if __name__ == "__main__":
  t = read_int()[0]
  for i in range(t):
    solve(i)