def solve():
  t = int(input())
  for case in range(1, t + 1):
    s = input()
    nums = list(map(int, s))
    stack = []
    ret = ''
    for x in nums:
      while len(stack) < x:
        stack.append('(')
        ret += '('
      while len(stack) > x:
        stack.pop()
        ret += ')'
      ret += str(x)
    ret += ''.join([')'] * len(stack))
    print('Case #{}: {}'.format(case, ret))

if __name__ == '__main__':
  solve()