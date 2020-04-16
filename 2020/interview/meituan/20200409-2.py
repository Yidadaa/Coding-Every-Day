def read_ints():
  return list(map(int, input().split(' ')))

def solve():
  n = int(input())
  start_order = read_ints()
  arrive_order = read_ints()

  rerank = [0] * (n + 1)
  for i in range(n): rerank[start_order[i]] = i

  m = rerank[arrive_order[-1]]
  ret = 0
  for i in range(n - 1, -1, -1):
    ret += int(m < rerank[arrive_order[i]])
    m = min(m, rerank[arrive_order[i]])
  print(ret)

if __name__ == '__main__':
  solve()
