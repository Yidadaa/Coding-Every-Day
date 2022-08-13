def solution(x, y):
    x, y = int(x), int(y)
    x, y = min(x, y), max(x, y)

    count = 0
    while x > 0 and y > 1:
        count += y // x
        x, y = y % x, x
        x, y = min(x, y), max(x, y)
    return str(max(0, count - 1)) if y == 1 else 'impossible'

for case in [[4, 7], [2, 1], [2, 4], [1, 1], [2, 2], [1, 5], [3, 5],
        [47068900554068939361891195233676009091941690850, 76159080909572301618801306271765994056795952743],
        [47068900554068939361891195233676009091941690850, 42342342343243242342343278]]:
    print(case, solution(*case))