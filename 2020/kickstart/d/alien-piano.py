def read_ints():
  return list(map(int, input().split(' ')))

def solve():
  t = int(input())
  for case in range(1, t + 1):
    n = int(input())
    nums = read_ints()
    state = [0, 0, 0, 0]
    for i in range(1, n):
      next_state = [0, 0, 0, 0]
      if nums[i] == nums[i - 1]: continue
      if nums[i] > nums[i - 1]:
        for j in range(1, 4):
          next_state[j] = min(state[:j])
        next_state[0] = min(state) + 1
      else:
        for j in range(3):
          next_state[j] = min(state[j + 1:])
        next_state[3] = min(state) + 1
      state = next_state
    print('Case #{}: {}'.format(case, min(state)))

if __name__ == '__main__':
  solve()

'''
6
5
1 5 100 500 1
8
2 3 4 5 6 7 8 9
8
2 1 0 -1 -2 2 3 4
16
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
12
1 2 3 4 3 2 1 2 3 4 3 2 1
3
1 2 3
'''

'''
0
1
1
3
0
0
'''