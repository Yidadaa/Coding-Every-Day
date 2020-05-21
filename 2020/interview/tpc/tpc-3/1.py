def solve():
    T = int(input())
    #         0  1  2  3  4  5  6  7  8  9  10 11 12 13
    primes = [0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1]

    table = {
        'divide_by_three': 3,
        'divide_by_four': 4,
        'divide_by_five': 5
    }

    for i in range(T):
        h, command = input().split(' ')
        h = int(h)
        if command in table:
            for i in range(5):
                if (h + i) % table[command] == 0:
                    print(i)
                    break
        else:
            for i in range(5):
                if primes[h + i]:
                    print(i)
                    break


solve()