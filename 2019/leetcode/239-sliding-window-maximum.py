class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        q, ret = [], []
        l, r = -1, -1
        n = len(nums)
        
        while r < n - 1:
            r += 1
            while len(q) > 0 and nums[q[-1]] < nums[r]:
                q.pop()
            q.append(r)
            
            if r - l >= k:
                if l == q[0]: q.pop(0)
                ret.append(nums[q[0]])
                l += 1
                
        return ret
