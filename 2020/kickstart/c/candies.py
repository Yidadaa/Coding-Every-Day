def read_ints():
    return list(map(int, input().split(' ')))

class Prefix():
    def __init__(self, nums):
        self.arr = [0] * (len(nums) + 1)
        self.sarr = [0] * (len(nums) + 1)
        self.aarr = [0] * (len(nums) + 1)
        self.nums = nums
        for i in range(1, len(nums) + 1):
            self.add(i, nums[i - 1])
        # print(self.aarr)
        # print(self.sarr)

    def update(self, i: int, val: int) -> None:
        self.add(i, val - self.nums[i - 1])
        self.nums[i - 1] = val

    def add(self, i: int, val: int):
        neg = 1 if i % 2 else -1
        aval = val * neg
        sval = val * neg * i
        while i < len(self.arr):
            self.arr[i] += val
            self.aarr[i] += aval
            self.sarr[i] += sval
            i += (i & -i)

    def get(self, i):
        val_sum, sweet_sum = 0, 0
        ret = 0
        li = i
        while i > 0:
            ret += self.arr[i]
            val_sum += self.aarr[i]
            sweet_sum += self.sarr[i]
            i -= (i & -i)
        return sweet_sum, val_sum

    def sumRange(self, i: int, j: int) -> int:
        sl, vl = self.get(i - 1)
        sr, vr = self.get(j)
        # print(sr, vr)
        # print(sl, vl)
        val_sum, sweet_sum = vr - vl, sr - sl
        return (sweet_sum - (i - 1) * val_sum) * (1 if i % 2 else -1)


def solve():
    T = int(input())
    for t in range(1, T + 1):
        n, q = read_ints()
        nums = read_ints()
        # tree = SweetTree(nums)
        tree = Prefix(nums)
        ret = 0
        for i in range(q):
            action, a, b = input().split(' ')
            if action == 'Q':
                ret += tree.sumRange(int(a), int(b))
            elif action == 'U':
                tree.update(int(a), int(b))
        print('Case #{}: {}'.format(t, ret))

solve()


'''
2
5 4
1 3 9 8 2
Q 2 4
Q 5 5
U 2 10
Q 1 2
3 3
4 5 5
U 1 2
U 1 7
Q 1 2
'''