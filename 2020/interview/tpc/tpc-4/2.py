def read_ints():
    return list(map(int, input().split(' ')))

def solve():
    T = int(input())
    for t in range(T):
        n = int(input())
        nums = read_ints()
        sort_nums = sorted(nums)
        halfn = n // 2
        mid = (sort_nums[n // 2 - 1] + sort_nums[n // 2]) / 2
        # print(mid)
        lc, rc = [], []
        le, re = [], []
        for i in range(n):
            if i < halfn:
                if nums[i] > mid:
                    lc.append(i)
                elif nums[i] == mid:
                    le.append(i)
            else:
                if nums[i] < mid:
                    rc.append(i)
                elif nums[i] == mid:
                    re.append(i)
        ls = sum(lc)
        rs = sum(rc)
        if len(lc) < len(rc):
            for i in range(len(rc) - len(lc)):
                ls += le[len(le) - 1 - i]
        elif len(lc) > len(rc):
            for i in range(len(lc) - len(rc)):
                rs += re[i]
        print(abs(rs - ls))

solve()

'''
4
4
1 2 3 4
4
4 3 2 1
4
2 1 1 1
8
4 4 4 1 1 1 5 6
'''