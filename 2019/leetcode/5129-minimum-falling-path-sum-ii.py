class Solution(object):
    def minFallingPathSum(self, arr):
        """
        :type arr: List[List[int]]
        :rtype: int
        """
        m, n = len(arr), len(arr[0])
        MAX = 100
        
        for i in range(1, m):
            for j in range(n):
                arr[i][j] += min(arr[i - 1][:j] + arr[i - 1][j + 1:])
        return min(arr[-1])