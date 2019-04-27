class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        d = {}
        for i in range(len(nums)):
            x = nums[i]
            if x in d and i - d[x] <= k:
                return True
            d[x] = i
        return False
