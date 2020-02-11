class Solution:
    def maxJumps(self, arr: List[int], d: int) -> int:
        n = len(arr)
        tree = [[] for i in range(n)]
        
        for i in range(n):
            l = max(0, i - d)
            r = min(i + d + 1, n)
            
            for st, ed, step in [(i - 1, l - 1, -1), (i + 1, r, 1)]:
                for j in range(st, ed, step):
                    if arr[j] < arr[i]:
                        tree[j].append(i)
                    else:
                        break
                
        dp = [1] * n
        sorted_arr = sorted([(arr[i], i) for i in range(n)], key=lambda x: x[0])

        for _, i in sorted_arr:
            for j in tree[i]:
                dp[j] = max(dp[j], dp[i] + 1)
        return max(dp)

'''
两个关键点：
1. 审题，只能跳到比自己底的地方，一旦发现比自己高的就 beak，否则会超时；
2. 方法，一维 dp 就能解决，用 BFS 超时。
'''