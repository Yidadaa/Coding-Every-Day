class Solution:
    def jump(self, nums):
        n = len(nums)
        dp = [n] * n
        dp[-1] = 0
        for i in range(n - 1, -1, -1):
            for j in range(i, min(i + nums[i] + 1, n)):
                dp[i] = min(dp[j] + 1, dp[i])
        return dp[0]

if __name__ == '__main__':
    print(Solution().jump([1, 2, 3, 4, 5, 7]))