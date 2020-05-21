
def read_ints():
    return list(map(int, input().split(' ')))

def solve():
    n, first = input().split(' ')
    candies = read_ints()
    count = {}
    for c in candies: count[c] = count.get(c, 0) + 1

    group = [0, 0, 0]
    for c in count:
        group[0 if count[c] == 1 else 1 if count[c] == 2 else 2] += 1

    if group[-1] == sum(group):
        print('Bob')
        return

    if group[0] == 0 and group[1] == 1 and first == 'Bob':
        print('Bob')
        return

    print('Alice')
    return

solve()