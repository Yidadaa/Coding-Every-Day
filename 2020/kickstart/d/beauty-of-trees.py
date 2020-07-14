def read_ints():
  return list(map(int, input().split(' ')))

def solve():
  t = int(input())
  for case in range(1, t + 1):
    n, a, b = read_ints()
    tree = [[]] * (n)
    A = [1] * n
    B = [1] * n
    nums = read_ints()
    count = 0
    for i in range(n):
      tree[nums[i] - 1].append(i)
      ax = nums[i] - 1
      if ax >= a: A[ax] += A[ax - a]
      bx = nums[i] - 1
      if bx >= b: B[bx] += B[bx - b]
      count += A[ax] + B[bx]

    print('Case #{}: {}'.format(case, ))

if __name__ == '__main__':
  solve()