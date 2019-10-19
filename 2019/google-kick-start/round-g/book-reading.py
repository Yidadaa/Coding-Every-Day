from collections import Counter

off_line = True
inputs = '''3
11 1 2
8
2 3
11 11 11
1 2 3 4 5 6 7 8 9 10 11
1 2 3 4 5 6 7 8 9 10 11
1000 6 1
4 8 15 16 23 42
1
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
  n, m, q = read_int()
  torn_pages = read_int()
  readers = read_int()

  pages = 0

  reader_group = Counter(readers)

  if n > m:
    for read_page, count in reader_group.items():
      s = n // read_page
      for torn_page in torn_pages:
        if torn_page % read_page == 0: s -= 1
      pages += s * count

  print('Case #{}: {}'.format(case + 1, pages))

if __name__ == "__main__":
  t = read_int()[0]
  for i in range(t):
    solve(i)