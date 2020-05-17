def read_ints():
    return list(map(int, input().split(' ')))

def solve():
    T = int(input())
    for t in range(T):
        n, k = read_ints()
        nums = read_ints()
        i = 0
        ret = 0
        while i < len(nums):
            if nums[i] != k:
                i += 1
                continue
            ck = k
            while i < len(nums) and ck == nums[i] and ck > 0:
                i += 1
                ck -= 1
            ret += int(ck == 0)
        print('Case #{}: {}'.format(t + 1, ret))

solve()