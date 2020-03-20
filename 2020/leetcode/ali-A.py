'''
给出 n 张不同花色和牌面的扑克牌，其中牌面的取值范围是 [A, 10]，
即仅可能从 A - 10 的扑克牌中取牌，每个牌面最多有四种花色，所以 n >= 0 and n <= 40，
假如你每次都能出单牌、对子、顺子（5 张连续牌）、连对（3 个连续对子），问手上的牌最少
出多少次可以出完。
'''

def solve(cards):
  ret = 1 << 32
  q = [(cards, 0)]
  while q:
    cards, cnt = q.pop(0)
    if sum(cards) == 0:
      ret = min(ret, cnt)
      continue
    if cnt >= ret: continue
    for ncards in get_next(cards):
      q.append((ncards, cnt + 1))
  print(ret)

def get_next(cards):
  ncards = []
  for n, step, t in [(8, 3, 2), (6, 5, 1), (10, 1, 2), (10, 1, 1)]:
    for i in range(n):
      if all(cards[j] >= t for j in range(i, i + step)):
        ncards.append(cards.copy())
        for j in range(i, i + step): ncards[-1][j] -= t
        break

  return ncards

if __name__ == "__main__":
  solve([1, 1, 1, 2, 2, 2, 2, 2, 1, 1])
