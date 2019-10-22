class Solution:
    def search(self, nums:list, target: int) -> bool:
        if len(nums) == 0: return -1
        break_index = self.bi_search(lambda m: nums[m] < nums[-1], 0, len(nums) - 1)
        search_left = self.bi_search(lambda m: nums[m] >= target, 0, break_index - 1)
        search_right = self.bi_search(lambda m: nums[m] >= target, break_index, len(nums) - 1)
        return search_left if nums[search_left] == target else search_right if nums[search_right] == target else -1
        
    def bi_search(self, cond, l, r):
        while l < r:
            m = (l + r) >> 1
            if cond(m): r = m
            else: l = m + 1
        return l