class Solution:
    def numberOfSubarrays(self, nums: List[int], k: int) -> int:
        sum_prefix = [0]
        for n in nums: sum_prefix.append(sum_prefix[-1] + (n & 1))
        
        ret = 0
        h = {}
        for s in sum_prefix:
            if s not in h: h[s] = 0
            h[s] += 1
            if s - k in h: ret += h[s - k]
        
        return ret