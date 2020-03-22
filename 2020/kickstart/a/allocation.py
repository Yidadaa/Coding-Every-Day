def read_ints():
  return list(map(int, input().split(' ')))

def solve():
  k = int(input())
  for i in range(1, k + 1):
    n, dollars = read_ints()
    houses = read_ints()
    houses.sort()
    s, cnt = 0, 0
    for x in houses:
      s += x
      if s <= dollars:
        cnt += 1
      else: break
    print('Case #{}: {}'.format(i, cnt))

if __name__ == "__main__":
  solve()