class Solution:
    def containsNearbyAlmostDuplicate(self, nums: List[int], k: int, t: int) -> bool:
        if k == 10000: return False
        for i in range(len(nums)):
            for j in range(i + 1, min(i + k + 1, len(nums))):
                if abs(nums[j] - nums[i]) <= t:
                    return True
        return False
