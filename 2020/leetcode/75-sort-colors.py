class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        ri = 0
        bi = len(nums) - 1

        i = 0
        while i < len(nums):
            while ri < len(nums) and nums[ri] == 0: ri += 1
            while bi >= 0 and nums[bi] == 2: bi -= 1
            if i < ri and nums[i] == 0\
                or i >= ri and i <= bi and nums[i] == 1\
                or i > bi and nums[i] == 2:
                i += 1
            elif nums[i] == 0:
                nums[ri], nums[i] = nums[i], nums[ri]
                ri += 1
            elif nums[i] == 2:
                nums[bi], nums[i] = nums[i], nums[bi]
                bi -= 1

'''
双指针变种。
'''