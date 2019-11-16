class Solution:
    def numberOfWays(self, num_people: int) -> int:
        dp = [1, 1] + [0] * 1000
        
        for i in range(2, num_people // 2 + 1):
            for j in range(0, i):
                dp[i] += dp[j] * dp[i - 1 - j]
                
        return dp[num_people // 2] % (1000000000 + 7)
