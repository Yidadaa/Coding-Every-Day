def solution(x, y):
    s = x + y - 2
    return str(s * (s + 1) // 2 + x)

for i in range(1, 6):
    for j in range(1, 11):
        print(i, j, solution(i, j))
    print()