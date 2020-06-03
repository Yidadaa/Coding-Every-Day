def szero(n):
    return ''.join(['0'] * n)

def fill(s):
    return szero(4 - len(s)) + s

def form(s):
    return ':'.join(list(map(fill, s.split(':'))))

def solve():
    t = int(input())
    for i in range(t):
        s = input()
        if '::' in s:
            part = s.split('::')
            part = [form(p) for p in part]
            zeros = 32 - sum(len(p.replace(':', '')) for p in part)
            zeros //= 4
            zeros = ':'.join(['0000'] * zeros)
            part.insert(1, zeros)
            part = [p for p in part if len(p) > 0]
            print(':'.join(part))
        else:
            print(form(s))

solve()