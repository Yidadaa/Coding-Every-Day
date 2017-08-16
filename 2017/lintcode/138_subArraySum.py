class Solution:
    """
    @param nums: A list of integers
    @return: A list of integers includes the index of the first number 
             and the index of the last number
    """
    def subarraySum(self, nums):
        # 若sum(0, i) = sum(0, j)，则sum(i+1, j) = 0。
        sums = {}
        s = 0
        for i in range(len(nums)):
            s += nums[i]
            if s == 0:
                return [0, i]
            if s in sums:
                return [sums[s] + 1, i]
            else:
                sums[s] = i

print(Solution().subarraySum([2, 1, -1, -2]))