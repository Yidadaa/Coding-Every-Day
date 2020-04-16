def read_ints():
  return list(map(int, input().split(' ')))

def solve():
  t = int(input())
  for case in range(1, t + 1):
    n = int(input())
    a = read_ints()
    v = read_ints()

    a = list(range(n))
    m = [1 << 32]
    m_ = sum(v)

    def perm(nums, l):
      if l >= len(nums):
        if any(nums[i] == a[i] for i in range(n)): return
        m[0] = min(sum(abs(nums[i] - a[i]) * v[i] for i in range(n)), m[0])
        return

      for i in range(l, len(nums)):
        nums[i], nums[l] = nums[l], nums[i]
        if nums[i] == a[i] or nums[l] == a[l] or m[0] == m_: continue
        perm(nums.copy(), l + 1)

    perm(a.copy(), 0)
    print(m[0])

if __name__ == '__main__':
  solve()


'''
1
10
1 2 3 4 5
1 4 1 1 1 1 1 1 1 1
'''