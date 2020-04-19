def read_ints():
  return list(map(int, input().split(' ')))

def solve():
  t = int(input())
  for case in range(1, t + 1):
    n = int(input())
    nums = read_ints()
    ret = sum(nums[i - 1] < nums[i] and nums[i] > nums[i + 1] for i in range(1, n - 1))
    print('Case #{}: {}'.format(case, ret))

if __name__ == '__main__':
  solve()

'''
4
3
10 20 14
4
7 7 7 7
5
10 90 20 90 10
3
10 3 10
'''