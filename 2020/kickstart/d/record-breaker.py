def read_ints():
  return list(map(int, input().split(' ')))

def solve():
  t = int(input())
  for case in range(1, t + 1):
    n = int(input())
    nums = read_ints()
    last_max = -1
    count = 0
    for i in range(n):
      if nums[i] > last_max and (i == n - 1 or nums[i] > nums[i + 1]):
        count += 1
      last_max = max(nums[i], last_max)

    print('Case #{}: {}'.format(case, count))

if __name__ == '__main__':
  solve()

'''
4
8
1 2 0 7 2 0 2 0
6
4 8 15 16 23 42
9
3 1 4 1 5 9 2 6 5
6
9 9 9 9 9 9
'''