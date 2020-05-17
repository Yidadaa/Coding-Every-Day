def read_ints():
    return list(map(int, input().split(' ')))

class Node:
    def __init__(self, l, r):
        self.l = l
        self.r = r
        self.lchild = None
        self.rchild = None
        self.val = 0
        self.sweet = 0

class SweetTree:

    def __init__(self, nums):
        self.nums = nums
        self.tree = self.build(0, len(nums) - 1)
        self.q = [None] * len(self.nums)
        self.cache = {}

    def build(self, l, r):
        if l > r: return None
        node = Node(l, r)
        if l == r:
            node.sweet = self.nums[l] * (l + 1) * (-1 if l % 2 else 1)
            node.val = self.nums[l] * (-1 if l % 2 else 1)
            return node
        m = (l + r) >> 1
        node.lchild = self.build(l, m)
        node.rchild = self.build(m + 1, r)
        node.sweet = node.lchild.sweet + node.rchild.sweet
        node.val = node.lchild.val + node.rchild.val
        return node

    def update(self, i: int, val: int) -> None:
        self.cache = {}
        i -= 1
        d = val - self.nums[i]
        self.nums[i] = val
        self.q[0] = self.tree
        count = 1
        while count:
            node = self.q[count - 1]
            count -= 1
            if i >= node.l and i <= node.r:
                node.val += d * (-1 if i % 2 else 1)
                node.sweet += d * (i + 1) * (-1 if i % 2 else 1)
            else: continue
            for child in [node.lchild, node.rchild]:
                if child:
                    self.q[count] = child
                    count += 1

    def sumRange(self, i: int, j: int):
        i -= 1
        j -= 1
        if (i, j) in self.cache: return self.cache[(i, j)]
        val_sum = 0
        sweet_sum = 0
        self.q[0] = self.tree
        count = 1
        while count:
            node = self.q[count - 1]
            count -= 1
            if node.l >= i and node.r <= j:
                val_sum += node.val
                sweet_sum += node.sweet
                continue
            if node.l > j or node.r < i: continue
            for child in [node.lchild, node.rchild]:
                if child and not (child.l > j or node.r < i):
                    self.q[count] = child
                    count += 1
        ret = (sweet_sum - i * val_sum) * (-1 if i % 2 else 1)
        self.cache[(i, j)] = ret
        return ret

class Prefix():
    def __init__(self, nums):
        self.arr = [0] * (len(nums) + 1)
        self.sarr = [0] * (len(nums) + 1)
        self.aarr = [0] * (len(nums) + 1)
        self.nums = nums
        for i in range(1, len(nums) + 1):
            self.add(i, nums[i - 1])

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
        sl, vl = self.get(j)
        sr, vr = self.get(i - 1)
        val_sum, sweet_sum = vr - vl, sr - sl
        return (sweet_sum - (i - 1) * val_sum) * (-1 if i % 2 else 1)


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