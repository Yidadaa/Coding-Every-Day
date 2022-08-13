
def xors(x):
    if x % 2 == 1:
        return (x + 1) // 2 % 2
    return xors(x + 1) ^ (x + 1)

def xorr(s, t):
    return xors(t) ^ xors(s - 1)

def solution(start, length):
    st = start
    ret = 0
    for i in range(length, 0, -1):
        ret ^= xorr(st, st + i - 1)
        st += length
    return ret

for case in [[0, 3], [17, 4]]:
    print(case, solution(*case))