
def solve():
    votes = input().split(',')
    count = {}
    if len(votes) >= 100 or len(votes) == 0:
        print('error.0001')
        return
    for name in votes:
        if len(name) == 0\
                or name[0] < 'A' or name[0] > 'Z'\
                or name[1:] != name[1:].lower():
            print('error.0001')
            return
        count[name] = count.get(name, 0) + 1
    max_item = ('', 0)
    for item in count.items():
        if item[1] > max_item[1]\
                or item[1] == max_item[1] and item[0] < max_item[0]:
            max_item = item
    print(max_item[0])


solve()

'''
1. 非法输入
sfsd,fsdf
Ta,Tas,
TaT,TaT
T,A,B

2. 测试
Tom,Lily,Tom,Lucy,Lucy,Jack
Tom,Lily,Tom,Lucy,Lucy,Jack,Tom
'''
