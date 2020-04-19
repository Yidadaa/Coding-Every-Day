def read_ints():
  return list(map(int, input().split(' ')))

def solve():
  t = int(input())
  table = {
    'S': 0,
    'W': 1,
    'N': 2,
    'E': 3
  }
  MOD = 1000000000
  for case in range(1, t + 1):
    moves = input()
    repeat = []
    pos = [[0, 0, 0, 0]] # s w n e
    i = 0
    while i < len(moves):
      m = moves[i]
      if '2' <= m <= '9':
        repeat.append(int(m))
        pos.append([0, 0, 0, 0])
        i += 1
      elif m == ')':
        r = repeat.pop()
        for j in range(4): pos[-2][j] = (pos[-2][j] + pos[-1][j] * r) % MOD
        pos.pop()
      else:
        pos[-1][table[m]] += 1
      i += 1
    pos = pos.pop()
    ms, me = pos[0] - pos[2], pos[3] - pos[1]
    ms %= MOD
    me %= MOD
    print('Case #{}: {} {}'.format(case, me + 1, ms + 1))

if __name__ == '__main__':
  solve()

'''
1
N3(S)N2(E)N
'''