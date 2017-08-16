class Solution:
    # @param A, a list of integers
    # @return an integer
    def jump(self, A):
        # 最好情况是o(n)，最坏是o(n^2)
        length = len(A)
        if length <= 1:
            return length
        path = {}
        maxIndex = 0
        count = 0
        for i in range(length):
            tmp = i + A[i]
            maxIndex = tmp if tmp > maxIndex else maxIndex # 保存最大跳跃距离，用于检测是否能到达终点
            if tmp in path:
                path[tmp].append(i)
            else:
                path[tmp] = [i] # 把所有能到达tmp的节点保存起来
            if (A[i] == 0 and maxIndex <= i) or (i == length - 1 and maxIndex < i):
                # 表示跳不过去
                return 0 # 直接返回零次
        i = length - 1
        while i > 0:
            # path存储的是能够到达某节点的所有可能的前向节点
            minIndex = length
            for node in filter(lambda x: x >= i, path.keys()):
                # 对path中能够到达i的节点进行过滤，寻找最小的节点
                minIndex = path[node][0] if path[node][0] < minIndex else minIndex
            i = minIndex
            count += 1
        return count

test = [[2,3,1,1,4], [1,2,1,0,1,2], [1,2,4,2,3,4]]
print(list(map(lambda x:Solution().jump(x), test)))