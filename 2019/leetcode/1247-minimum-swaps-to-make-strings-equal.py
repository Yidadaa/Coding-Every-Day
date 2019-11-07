class Solution:
    def minimumSwap(self, s1: str, s2: str) -> int:
        if len(s1) != len(s2): return -1

        c_1 = self.count(s1)
        c_2 = self.count(s2)
        
        if (c_1['x'] + c_2['x']) % 2 or (c_1['y'] + c_2['y']) %2:
            return -1
        
        c = {'xy': 0, 'yx': 0}
        for ch1, ch2 in zip(s1, s2):
            if ch1 != ch2: c[ch1 + ch2] += 1
        
        ret = 0
        ret += c['xy'] // 2 + c['yx'] // 2
        if c['xy'] & 1 == c['yx'] & 1:
            ret += 2 * (c['xy'] & 1) * (c['yx'] & 1)
        else:
            ret = -1
        return ret
        
    def count(self, s):
        count = {'x': 0, 'y': 0}
        for c in s: count[c] += 1
        return count