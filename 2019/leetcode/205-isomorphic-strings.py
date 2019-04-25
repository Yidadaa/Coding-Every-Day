class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        return self.recode(s) == self.recode(t)
        
    def recode(self, s):
        s = list(s)
        d = self.count(s)
        target = []
        for c in s:
            target.append(d[c])
        return target
        
    def count(self, nums):
        ret = {}
        i = 0
        for x in nums:
            if x not in ret:
                ret[x] = i
                i += 1
        return ret

'''
Tips:
1. 我用的方法很常规，直接对两组字符串进行重编码，编码表以每个字符出现的次序为主
2. 排名第一的答案很有启发性，两个字符串是否同构，只需判断两者相应位置的字符形成的元组是否能与每一个字符一一对应即可
第一的参考代码：`len(set(zip(s, t))) == len(set(s)) == len(set(t))`
'''