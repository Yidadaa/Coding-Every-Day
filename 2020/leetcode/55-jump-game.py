class Solution:
    def canJump(self, nums):
        n = len(nums)
        ed = n - 1
        for i in range(n - 1, -1, -1):
            if i + nums[i] >= ed: ed = i
        return ed == 0

if __name__ == '__main__':
    print(Solution().canJump([3,2,1,0,4]))