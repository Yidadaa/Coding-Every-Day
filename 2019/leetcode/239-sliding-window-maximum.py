class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        ret = []
        
        if len(nums) == 0 or k == 0:
            return ret
        
        if k == 1:
            return nums
        
        q = [0]
        l, r = 0, 0
        while r < len(nums) - 1:
            r += 1
            while len(q) > 0 and nums[q[-1]] < nums[r]:
                q.pop()
            q.append(r)
            if r - l + 1 == k:
                ret.append(nums[q[0]])
            elif r - l + 1 > k:
                if l == q[0]:
                    q.pop(0)
                ret.append(nums[q[0]])
                l += 1
        return ret
