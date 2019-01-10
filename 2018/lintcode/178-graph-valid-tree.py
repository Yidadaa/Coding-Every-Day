class Solution:
    """
    @param n: An integer
    @param edges: a list of undirected edges
    @return: true if it's a valid tree, or false
    """
    def validTree(self, n, edges):
        # 如果无向图可以成树，那么一定满足以下条件：
        # 1. 从一个节点出发进行遍历，一定能遍历所有的边
        # 2. 从一个节点出发进行遍历，每个节点仅能遍历一次
        # 3. 所有的节点都能被遍历到
        # 过滤掉特殊情况
        if n <= 0:
            return False
        if n == 1 and len(edges) == 0:
            return True
        # 用来保存每个节点的相邻边
        degrees = [[] for i in range(n)]
        traversed = [0 for e in edges]
        for i in range(len(edges)):
            e = edges[i]
            degrees[e[0]].append(i)
            degrees[e[1]].append(i)
        # 剔除掉孤立点
        for d in degrees:
            if len(d) == 0:
                return False
        stack = [0]
        traversedNodes = set()
        # 开始宽度优先遍历
        while len(stack) > 0:
            nextNode = stack.pop()
            if nextNode in traversedNodes:
                # 如果节点已经遍历过，那么证明一定不是树木
                return False
            traversedNodes.add(nextNode)
            for e in degrees[nextNode]:
                if not traversed[e]:
                    # 标记已经遍历的边
                    traversed[e] = 1
                    stack.append(edges[e][0] if edges[e][0] != nextNode else edges[e][1])
        for e in traversed:
            # 如果有的边没有被遍历过，证明该无向图存在不连通的节点或者区域
            if e == 0:
                return False
        return True

if __name__ == '__main__':
    print(Solution().validTree(10, [[0,1],[5,6],[6,7],[9,0],[3,7],[4,8],[1,8],[5,2],[5,3]]))
