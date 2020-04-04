def read_ints():
  return list(map(int, input().split(' ')))

def solve():
  t = int(input())
  d = {
    'C': 'J',
    'J': 'C'
  }
  for case in range(1, t + 1):
    n = int(input())
    times = []
    for i in range(n):
      times.append(read_ints() + [i])
    times.sort(key=lambda x: x[0])
    ret = [None] * n
    for i in range(n):
      if not ret[times[i][-1]]: ret[times[i][-1]] = 'C'
      last = ret[times[i][-1]]
      ni = i + 1
      while ni < n and times[ni][0] < times[i][1]:
        if ret[times[ni][-1]] == last:
          ret = ['IMPOSSIBLE']
          break
        ret[times[ni][-1]] = d[last]
        ni += 1
      if ret[0] == 'IMPOSSIBLE': break
    print('Case #{}: {}'.format(case, ''.join(ret)))

if __name__ == '__main__':
  solve()