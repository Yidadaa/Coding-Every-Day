def check(pegs, size):
    d = size
    for i in range(1, len(pegs)):
        d = pegs[i] - pegs[i - 1] - d
        if d < 1:
            return False
    return True

def solution(pegs):
    n = len(pegs)
    d = 0
    for i in range(1, n):
        d = pegs[i] - pegs[i - 1] - d 

    if n % 2 == 0:
        b = 3
        a = 2 * d
        if a % 3 == 0:
            a //= 3
            b //= 3
        size = float(a) / float(b)
        if size >= 1 and check(pegs, size):
            return [a, b]
    else:
        size = -2 * d
        if size >= 1 and check(pegs, size):
            return [size, 1]
    return [-1, -1]

for case in [[4, 30, 50], [4, 17, 50], [4, 30, 50, 80], [1, 26]]:
    print(case, solution(case))