def solve():
    T = int(input())

    t = {
        'T': 0,
        'P': 1,
        'C': 2
    }

    p = {
        'TPC': 0,
        'PTC': 1,
        'PCT': 2,
        'TCP': 1,
        'CTP': 1,
        'CPT': 1
    }

    MAX = 1 << 31

    for i in range(T):
        n = int(input())
        s = input()
        
        ltpc = [[-1, -1, -1] for i in range(n)]
        rtpc = ltpc.copy()

        for i in range(n):
            if s[i] not in t: continue
            if i > 0:
                ltpc[i] = ltpc[i - 1]
            ltpc[i][t[s[i]]] = i
        
        for i in range(n - 1, -1, -1):
            if s[i] not in t: continue
            if i < n - 1:
                rtpc[i] = rtpc[i + 1]
            rtpc[i][t[s[i]]] = i

        ret = MAX
        for i in range(n):
            if s[i] not in t: continue
            for tpt in p:
                count = p[tpt]
                prime_index = tpt.index(s[i])
                for j in range(3):
                    if tpt[j] == s[i]: continue
                    if j < prime_index:
                        if ltpc[i][t[tpt[j]]] < 0:
                            count = MAX
                            break
                        count += int(abs(ltpc[i][t[tpt[j]]] - i) > 1)
                    elif j > prime_index:
                        if rtpc[i][t[tpt[j]]] < 0:
                            count = MAX
                            break
                        count += int(abs(rtpc[i][t[tpt[j]]] - i) > 1)
                ret = min(count, ret)
                print(tpt, count)
        print(ret if ret != MAX else 'Impossible')

solve()