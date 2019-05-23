class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        ret = nums[0]
        s = 0
        for x in nums:
            print(s, x, s + x)
            s = max(s + x, x)
            ret = max(ret, s)
        return ret
