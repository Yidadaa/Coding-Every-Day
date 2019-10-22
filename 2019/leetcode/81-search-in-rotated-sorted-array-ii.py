class Solution:
    def search(self, nums:list, target: int) -> bool:
        if len(nums) == 0: return False
        l, r = 0, len(nums) - 1
        while l < r and nums[l] == nums[l + 1]: l += 1
        while r > l and nums[r] == nums[r - 1]: r -= 1
        break_index = self.bi_search(lambda m: nums[m] < nums[-1], l, r, nums)
        search_left = self.bi_search(lambda m: nums[m] >= target, 0, break_index - 1, nums)
        search_right = self.bi_search(lambda m: nums[m] >= target, break_index, len(nums) - 1, nums)
        return nums[search_left] == target or nums[search_right] == target
        
    def bi_search(self, cond, l, r, nums):
        while l < r:
            m = (l + r) >> 1
            if cond(m): r = m
            else: l = m + 1
        return l


if __name__ == "__main__":
    cases = [
      ([1, 2, 3, 4, 5, 6], 4),
      ([1, 2, 3, 4, 5, 6], 0),
      ([2, 3, 4, 5, 6, 1], 4),
      ([2, 3, 4, 5, 6, 1], 0),
      ([3, 1, 1, 1], 3),
      ([2, 3, 2, 2, 2], 3)
    ]

    for c in cases:
      print(Solution().search(*c))