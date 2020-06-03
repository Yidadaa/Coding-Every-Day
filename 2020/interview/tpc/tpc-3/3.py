import math

def primes(n):
    flags = [1] * n
    for i in range(2, n):
        if not flags[i]: continue
        j = i
        while i * j < n:
            flags[i * j] = 0
            j += 1
    return flags

p = primes(10000000)

def is_prime(n):
    return p[n]

def check(n):
    if not is_prime(n): return False
    for i in range(len(n)):
        n = n[-1] + n[:-1]
        if not is_prime(n): return False
    return True

def check_r(s, m):
    ret = ''
    for i in range(len(s) - m):
        if check(s[i:i + m]): ret = s[i:i + m]
    return ret

def solve():
    T = int(input())
    nums = set(['1', '3', '7', '9'])
    for i in range(T):
        s = input()
        subs = []
        i = 0
        while i < len(s):
            if s[i] not in nums:
                i += 1
                continue
            part = ''
            while i < len(s) and s[i] in nums:
                part += s[i]
                i += 1
            if part: subs.append(part)
        print(subs)
        ret = 0
        for ss in subs:
            i, j = 1, len(ss)
            while i < j:
                m = (i + j) >> 1
                if check_r(ss, m): i = m + 1
                else: j = m
            print(i, ss, check_r(ss, i))
            sb = check_r(ss, i)
            ret = max(ret, int(sb) if sb else 0)
        print(ret)


solve()