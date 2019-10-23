class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        l, r = 0, len(nums) - 1

        while l < r:
            m = (l + r) >> 1
            if nums[m] >= target: r = m
            else: l = m + 1

        if len(nums) == 0 or nums[l] != target: return [-1, -1]

        ret_l = l

        l, r = l, len(nums) - 1
        while l < r:
            m = (l + r) >> 1
            if nums[m] >= target + 1: r = m
            else: l = m + 1

        ret_r = l if nums[l] == target else l - 1

        return [ret_l, ret_r]
