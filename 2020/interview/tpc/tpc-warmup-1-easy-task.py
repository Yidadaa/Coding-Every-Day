from bisect import insort

def read_ints():
    return list(map(int, input().split(' ')))

def solve():
    t = int(input())
    for i in range(t):
        n = input()
        nums = read_ints()
        nums.sort()
        while nums[0] != nums[-1]:
            x = nums.pop() - nums.pop(0)
            for i in range(2): insort(nums, x)
        print(nums[0])

solve()

'''
2
3
1 2 3
2
5 5
'''
