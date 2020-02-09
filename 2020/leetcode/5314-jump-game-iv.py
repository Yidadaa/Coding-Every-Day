class Solution:
    def minJumps(self, arr: List[int]) -> int:
        adj = [set() for i in arr]
        count = {}
        
        i = 0
        while i < len(arr):
            if arr[i] not in count:
                count[arr[i]] = []
            count[arr[i]].append(i)
            for a in count[arr[i]] + [i - 1, i + 1]:
                if a != i and a >= 0 and a < len(arr):
                    adj[i].add(a)
                    adj[a].add(i)
            if i < len(arr) - 1 and arr[i + 1] == arr[i]:
                while i < len(arr) - 1 and arr[i + 1] == arr[i]: i += 1
            else:
                i += 1
                
        flag = [True] * len(arr)
        queue = [(0, 0)]
        target = len(arr) - 1
        while len(queue) > 0:
            node, l = queue.pop(0)
            flag[node] = False
            if node == target:
                return l
            for adj_node in adj[node]:
                if flag[adj_node]:
                    queue.append((adj_node, l + 1))
        return -1