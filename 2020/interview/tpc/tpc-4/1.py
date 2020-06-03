def read_ints():
    return list(map(int, input().split(' ')))

MAX = 1 << 32
MIN = -MAX

def solve():
    T = int(input())
    for i in range(T):
        n = int(input())
        matrix = [[]] * n
        s = 0
        for i in range(n):
            matrix[i] = read_ints()
            s += sum(matrix[i]) * 2

        min_diag = MAX
        max_diag = MIN
        max_other = MIN
        center_diag = None
        for r in range(n):
            for c in range(n):
                if r == c or r + c == n - 1:
                    s += matrix[r][c]
                    if r == c and r + c == n - 1:
                        s += matrix[r][c]
                        center_diag = matrix[r][c]
                    else:
                        min_diag = min(min_diag, matrix[r][c])
                        max_diag = max(max_diag, matrix[r][c])
                else:
                    max_other = max(max_other, matrix[r][c])

        if min_diag != MAX and max_other != MIN:
            if center_diag is None:
                ds = max_other - min_diag
                if ds > 0: s += ds
            else:
                s = max(s, s + max_other - min_diag, s + 2 * (max_other - center_diag), s + max_diag - center_diag)
        print(s)
solve()

'''
3
3
5 9 5
9 1 9
5 9 5
3
1 1 1
1 100 1
1 1 1
3
9 1 9
1 1 1
9 1 9
'''