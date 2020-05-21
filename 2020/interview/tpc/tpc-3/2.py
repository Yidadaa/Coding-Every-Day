def repeat(s, n):
    return ''.join([s] * n)

def solve():
    T = int(input())
    for i in range(T):
        s = input()
        count = { '0': 0, '1': 0 }
        for c in s: count[c] += 1
        if count['0'] > 2 * count['1'] + 2:
            print('Impossible')
        elif 2 * count['1'] < count['0'] <= 2 * count['1'] + 2:
            ret = ''.join(['0'] * (count['0'] - 2 * count['1'])) + ''.join(['100'] * count['1'])
            print(ret)
        else:
            ret = ''.join(['100'] * (count['0'] // 2))
            extra_ones = count['1'] - count['0'] // 2
            extra_zero = count['0'] % 2
            if extra_zero and not extra_ones:
                ret = '0' + ret
            elif extra_zero and extra_ones:
                ret += '10'
                extra_ones -= 1
            ret = repeat('1', extra_ones) + ret
            print(ret)

solve()

'''
7
110
01110
000
00000011
0000011
000011
00011
'''