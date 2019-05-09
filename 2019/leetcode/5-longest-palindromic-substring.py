class Solution:
    def longestPalindrome(self, s: str) -> str:
        ret = [0, 0, 0]
        for i in range(len(s) - 1):
            s1 = self.checkAroundCenter(i, i, s)
            s2 = self.checkAroundCenter(i, i + 1, s)
            s_ = s1 if s1[2] > s2[2] else s2
            ret = s_ if s_[2] > ret[2] else ret
        return s[ret[0]:ret[1] + 1]
        
    def checkAroundCenter(self, L, R, s):
        if s[L] != s[R]:
            return [L, L, 0]
        while L >= 0 and R < len(s) and s[L] == s[R]:
            L -= 1
            R += 1
        return [L + 1, R - 1, R - L + 3]
        
'''
最朴素的思路：中心扩展法，时间复杂度O(n^2)
'''
