def read_ints():
    return list(map(int, input().split(' ')))

def solve():
    t = int(input())
    for i in range(t):
        n, m = read_ints()
        nums = read_ints()
        nums.sort()
        l, r = 0, 2 * m - 1
        ret = 0
        while m and l < r:
            ret += nums[l] * nums[r]
            l += 1
            r -= 1
            m -= 1
        print(ret)

solve()

'''
3
4 2
1 3 2 4
3 1
2 3 1
4 0
1 3 2 4
'''