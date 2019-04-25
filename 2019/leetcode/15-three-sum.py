class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        ret = set()
        a2s = lambda a: '_'.join([str(d) for d in a])
        s2a = lambda s: [int(c) for c in s.split('_')]
        
        sn = set(nums)
        if len(sn) == 1 and sum(sn) == 0 and len(nums) > 2:
            return [[0, 0, 0]]

        for i in range(0, len(nums)):
            rt = self.twoSum(nums[i + 1:], -nums[i])
            if len(rt) > 0:
                for r in rt:
                    ret.add(a2s([nums[i], r[0], r[1]]))
        return [s2a(s) for s in ret]
        
    def twoSum(self, nums, target):
        ret = []
        d = {}
        for x in nums:
            t = target - x
            if x in d:
                ret.append([d[x], x])
                del d[x]
            else:
                d[t] = x
        return ret

'''
Tips:
1. 将三数之和问题化为两数之和问题
2. 可以分情况讨论，三数之和为0的情况只有四种：
    PPN, PNN, P0N, 000
    分情况讨论即可，可以比此代码快一倍多
3. 本代码重点处理了全0的情况，来覆盖某些case
'''