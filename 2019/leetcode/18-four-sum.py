class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        ret = set()
        a2s = lambda a: '_'.join([str(d) for d in a])
        s2a = lambda s: [int(c) for c in s.split('_')]
        for i in range(0, len(nums)):
            rt = self.threeSum(nums[i + 1:], target - nums[i])
            if len(rt) > 0:
                for r in rt:
                    ret.add(a2s([nums[i], r[0], r[1], r[2]]))
        return [s2a(s) for s in ret]
        
    def threeSum(self, nums: List[int], target: int) -> List[List[int]]:
        ret = []
        for i in range(0, len(nums)):
            rt = self.twoSum(nums[i + 1:], target - nums[i])
            if len(rt) > 0:
                for r in rt:
                    ret.append([nums[i], r[0], r[1]])
        return ret
        
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
1. 没什么新意，搞成 three sum 就行了
'''