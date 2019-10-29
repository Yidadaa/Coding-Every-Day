class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        if len(nums) == 0: return 0
        l, r = 0, len(nums) - 1
        while l < r:
            m = (l + r) >> 1
            if nums[m] >= target: r = m
            else: l = m + 1
        if nums[l] >= target: return l
        if nums[l] < target: return len(nums)
