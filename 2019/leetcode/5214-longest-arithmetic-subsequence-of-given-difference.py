class Solution:
    def longestSubsequence(self, arr: List[int], difference: int) -> int:
        cache = {}
        for a in arr:
            if a not in cache: cache[a] = 1 - int(difference == 0) # 差值为0时特别考虑
            last_a = a - difference
            if last_a in cache:
                cache[a] = max(cache[last_a] + 1, cache[a])
        print(cache)
        return max(cache.values())
