def read_ints():
    return list(map(int, input().split(' ')))

def solve():
    t = int(input())
    for case in range(1, t + 1):
        n = int(input())
        matrix = []
        k, rc, cc = 0, 0, 0
        for i in range(n):
            matrix.append(read_ints())
            k += matrix[-1][i]
            rc += int(len(set(matrix[-1])) < n)
        for c in range(n):
            s = set()
            for r in range(n): s.add(matrix[r][c])
            cc += int(len(s) < n)
        print('Case #{}: {} {} {}'.format(case, k, rc, cc))

if __name__ == '__main__':
    solve()