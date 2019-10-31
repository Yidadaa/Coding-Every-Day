class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        m, n = len(obstacleGrid), len(obstacleGrid[0])
        if m * n == 0: return 0
        
        state = [0] * n
        state[0] = 1
        
        for i in range(m):
            line = obstacleGrid[i]
            for j in range(n):
                if line[j]: state[j] = 0
                else: state[j] += state[j - 1] if j > 0 else 0
                    
        return state[-1]