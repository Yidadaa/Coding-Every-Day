class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        g1 = self.group(nums1)
        g2 = self.group(nums2)
        ret = []
        if len(g1) < len(g2):
            [g1, g2] = [g2, g1]
        for x in g2:
            if x in g1:
                s = min(g1[x], g2[x])
                while s > 0:
                    ret.append(x)
                    s -= 1
        return ret
        
    def group(self, nums):
        ret = {}
        for x in nums:
            if x in ret:
                ret[x] += 1
            else:
                ret[x] = 1
        return ret

'''
Tips:
1. 使用原生的`collections`模块可以大大加快建表的速度
'''