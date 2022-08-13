def read_int():
    return int(input())

def read_ints():
    return list(map(int, input().strip().split(' ')))

def mid(arr):
    n = len(arr) // 2
    return (arr[n] + arr[~n]) / 2.0

t = read_int()

for case in range(t):
    n, m = read_ints()
    r = read_ints()
    r.sort()
    
    s = 0
    for i in range(m - 1):
        s += r.pop()
    s += mid(r)
    print(f"Case #{case + 1}: {s}")