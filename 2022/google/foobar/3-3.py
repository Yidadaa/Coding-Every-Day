

def solution(n):
    n = int(n)
    q = [(n, 0)]
    solved = {}
    while q:
        nq = []
        for x, count in q:
            if x in solved and solved[x] <= count or x < 1:
                continue
            solved[x] = count
            if x % 2:
                nq.append(((x + 1) // 2, count + 2))
                nq.append((x - 1, count + 1))
            else:
                nq.append((x // 2, count + 1))
        q = nq
    return solved[1] if 1 in solved else n

def solve2(n):
    n = int(n)
    count = 0
    path = []

    while n > 1:
        if n % 2 == 0:
            n //= 2
        else:
            if n & (n + 1) == 0 and (n + 1) // 2 < n - 1:
                n += 1
            else:
                n -= 1
        count += 1
        path.append(n)
    #print(path)

    return count

def solve3(n):
    n = int(n)
    
    def solve(x, solved):
        if x in solved:
            return solved[x]
        if x % 2:
            res = min(solve((x + 1) // 2, solved) + 2, solve(x - 1, solved) + 1)
        else:
            res = min(solve(x // 2, solved) + 1, solve(x - 1, solved) + 1)
        solved[x] = res
        return solved[x]

    return solve(n, {0: 0, 1: 0})

large_x = ''
for i in range(309):
    large_x += '9'

for case in [4, 13, 15, 21, large_x]:
    print(case, solution(case))

for x in range(1, 100):
    a = solution(x)
    b = solve3(x)
    if a != b:
        # continue
        print(x, a, b)