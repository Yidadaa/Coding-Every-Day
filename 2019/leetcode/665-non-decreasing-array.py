class Solution:
    def checkPossibility(self, nums: List[int]) -> bool:
        i, j = 0, len(nums) - 1
        while i < j and nums[i] <= nums[i + 1]: i += 1
        while i < j and nums[j] >= nums[j - 1]: j -= 1
        return j == i\
            or (j - i == 1\
                and (i == 0\
                     or j == len(nums) - 1\
                     or nums[i] <= nums[j + 1]\
                     or nums[i - 1] <= nums[j]))
