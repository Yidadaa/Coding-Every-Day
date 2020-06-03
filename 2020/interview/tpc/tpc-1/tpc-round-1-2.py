def read_mat():
    ret = []
    for i in range(3):
        ret.append(list(map(int, input())))
    return ret

def solve():
    t = int(input())
    for i in range(t):
        sr = read_mat()
        tr = read_mat()
        # check impossible
        impossible = False
        if sr[1][1] != tr[1][1]:
            impossible = True
        if set(sr[1]) != set(tr[1]):
            impossible = True
        if not (sr[0][1] != tr[0][1] and sr[2][1] != tr[2][1]) and not (sr[0][1] != tr[2][1] and sr[2][1] != tr[0][1]):
            impossible = True
        if impossible:
            print('impossible')
            continue
        ret = 0
        ret += int(sr[0][1] != tr[0][1]) + int(sr[1][0] != tr[1][0])
        srnums = [sr[0][0], sr[0][2], sr[2][0], sr[2][2]]
        trnums = [tr[0][0], tr[0][2], tr[2][0], tr[2][2]]
        

solve()

'''
4
123
456
789
231
456
789
457
213
689
257
361
489
927
641
358
297
651
384
123
456
789
123
456
789
'''