import math
import bisect

def read_ints():
    return list(map(int, input().split(' ')))

MAXT = 100 * 100000
m = [0] * 2 * MAXT

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

        table = m.copy()
        count = 0
        s = 0
        mins = 0
        table[MAXT] = 1
        for x in nums:
            s += x
            mins = min(mins, s)
            kn = min(bisect.bisect_right(ks, s - mins) + 1, len(ks))
            for j in range(kn):
                k = ks[j]
                count += table[MAXT + s - k]
            table[s + MAXT] += 1
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