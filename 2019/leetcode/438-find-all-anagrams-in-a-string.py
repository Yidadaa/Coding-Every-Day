class Solution(object):
    def findAnagrams(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: List[int]
        """
        ret = []
        d = self.count(p)
        lp = len(p)
        dt = self.count(s[0:lp])
        
        if dt == d:
            ret.append(0)
            
        i = 1
        
        while i + lp - 1 < len(s):
            if i > 0:
                c = s[i - 1]
                if dt[c] > 1:
                    dt[c] -= 1
                else:
                    del dt[c]

            if i + lp - 1 < len(s):
                c = s[i + lp - 1]
                if c in dt:
                    dt[c] += 1
                else:
                    dt[c] = 1
            if d == dt:
                ret.append(i)
            i += 1
            
        return ret
        
    def count(self, s):
        s = list(s)
        d = {}
        for c in s:
            if c in d:
                d[c] += 1
            else:
                d[c] = 1
        return d
        
