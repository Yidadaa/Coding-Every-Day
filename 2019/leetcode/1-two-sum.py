class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        d = {}
        for i in range(0, len(nums)):
            t = target - nums[i]
            if nums[i] in d:
                return [d[nums[i]], i]
            else:
                d[t] = i

'''
Tips:
最容易想到的解法是o(n log n)，但最优解法是o(n)的
'''