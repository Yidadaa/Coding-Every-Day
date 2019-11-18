import bisect

def read_lines():
  return [int(x) for x in input().split(' ')]

def _solve(papers, case):
  ret = []
  h = 0
  q = []

  for paper in papers:
    if paper > h: # 我fo了，加了这一行就能过
      bisect.insort(q, paper)
    while len(q) > 0 and q[0] <= h:
      q.pop(0)
    if len(q) > h: h += 1
    ret.append(str(h))

  print("Case #{}: {}".format(str(case), ' '.join(ret)))


if __name__ == "__main__":
  t = int(input())

  for i in range(t):
    n = input()
    papers = read_lines()
    _solve(papers, i + 1)
