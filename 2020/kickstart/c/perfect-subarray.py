import math
import bisect

def read_ints():
    return list(map(int, input().split(' ')))

def solve():
    T = int(input())
    for t in range(1, T + 1):
        n = int(input())
        nums = read_ints()

        mi, ma = 0, -(1 << 32)
        s = 0
        for x in nums:
            s += x
            mi = min(x, mi, s)
            ma = max(x, ma, s)
        
        R = int(math.sqrt(ma - mi))
        ks = [i * i for i in range(R + 1)]

        table = {0: 1}
        count = 0
        s = 0
        mins = 0
        for x in nums:
            s += x
            mins = min(mins, s)
            kn = min(bisect.bisect_right(ks, s - mins) + 1, len(ks))
            for j in range(kn):
                k = ks[j]
                if s - k in table:
                    count += table[s - k]
            table[s] = table.get(s, 0) + 1
        print('Case #{}: {}'.format(t, count))
        
solve()

'''
1
4
-10 -2 11 5

4
3
2 2 6
5
30 30 9 1 30
4
4 0 0 16
4
-10 -2 11 5
'''