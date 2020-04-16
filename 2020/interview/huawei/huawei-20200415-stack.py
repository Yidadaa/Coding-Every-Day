def read_ints():
    return list(map(int, input().split(' ')))

class Func:
    def __init__(self, cost, call):
        self.cost = cost
        self.call = call

def solve():
    meta = read_ints()
    n = meta[0]
    graph = {}
    for i in range(n):
        func = read_ints()
        if len(func) == 1: func.append(None)
        graph[func[0]] = Func(func[1], func[2:])
    # 查看是否存在未给出调用栈大小的函数
    if any(func.cost is None for func in graph.values()):
        print('NA')
        return
    # DFS 查找最大调用栈，同时判断是否存在递归
    maxcost = 0
    for func in graph:
        stack = [(func, set(), 0)]
        while stack:
            f, path, cost = stack.pop()
            if f in path:
                print('R')
                return
            cost += graph[f].cost
            maxcost = max(maxcost, cost)
            for child in graph[f].call:
                stack.append((child, path | set([f]), cost))
    print(maxcost)

solve()

'''
1. 常规 case
5 2 3 1 0 0
1 20 2 3
2 30 3 4 5
3 50 4
4 60
5 80

2. 带环 case
5 2 3 1 0 0
1 20 2 3
2 30 3 4 5
3 50 4
4 60
5 80 2

3. 未定义栈大小 case
5 2 3 0 0 0
1 20 2 3
2 30 3 4 5
3
4 60
5 80 2
'''
