def read_ints():
  return list(map(int, input().split(' ')))


class TreeArray:
  def __init__(self, nums):
    self.arr = [0] * (len(nums) + 1)
    self.nums = nums
    for i in range(1, len(nums) + 1):
      self.update(i, nums[i - 1])

  def update(self, i, val):
    while i < len(self.arr):
      self.arr[i] = max(self.arr[i], val)
      i += (i & -i)

  def get(self, l, r):
    ret = 0
    while r >= l:
      ret = max(self.arr[r], ret)
      r -= 1
      while r - (r & -r) >= l:
        ret = max(self.arr[r], ret)
        r -= (r & -r)
    return ret

def solve():
  t = int(input())
  for case in range(1, t + 1):
    n, q = read_ints()
    rooms = read_ints()
    tree = TreeArray(rooms)
    ret = [0] * q
    for qi in range(q):
      s, k = read_ints()
      for l, r in [[s - k, s], [s, s + k]]:
        while l < r:
          m = (l + r)
      ret[qi] = str(room + 1)
    print('Case #{}: {}'.format(case, ' '.join(ret)))

if __name__ == '__main__':
  solve()

'''
2
5 4
90 30 40 60
3 4
3 1
1 5
4 3
10 2
6 2 4 5 9 30 7 1 8
6 8
6 8
'''
