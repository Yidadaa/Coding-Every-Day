def solve():
    t = int(input())
    for i in range(t):
        n = int(input())
        print(max(1, n // 2))

if __name__ == "__main__":
    solve()