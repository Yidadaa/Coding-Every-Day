def read_ints():
    return list(map(int, input().split(' ')))

def solve():
    T = int(input())
    for t in range(1, T + 1):
        r, c = read_ints()
        wall = [list(input()) for i in range(r)]
        blocks = set()
        for line in wall:
            blocks |= set(line)
        graph = {b: [0, set()] for b in blocks}

        for i in range(r):
            for j in range(c):
                block = wall[i][j]
                if i >= r - 1: continue
                nblock = wall[i + 1][j]
                if nblock != block and block not in graph[nblock][1]:
                    graph[block][0] += 1
                    graph[nblock][1].add(block)
        ret = ''
        while graph:
            should_break = True
            for block in list(graph.keys()):
                if graph[block][0] > 0: continue
                should_break = False
                ret += block
                for sb in graph.pop(block)[1]:
                    graph[sb][0] -= 1
            if should_break: break
        ret = -1 if graph else ret
        print('Case #{}: {}'.format(t, ret))

solve()

'''
1
4 6
ZOAAMM
ZOAOMM
ZOOOOM
ZZZZOM

4
4 6
ZOAAMM
ZOAOMM
ZOOOOM
ZZZZOM
4 4
XXOO
XFFO
XFXO
XXXO
5 3
XXX
XPX
XXX
XJX
XXX
3 10
AAABBCCDDE
AABBCCDDEE
AABBCCDDEE
'''