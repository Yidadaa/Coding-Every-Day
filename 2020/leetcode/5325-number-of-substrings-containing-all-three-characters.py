class Solution:
    def numberOfSubstrings(self, s: str) -> int:
        t = {
            'a': -1,
            'b': -1,
            'c': -1
        }

        n = len(s)
        ret = 0
        for i in range(n):
            count = n
            for ch in "abc":
                if ch != s[i]: count = min(count, t[ch])
            ret += max(count + 1, 0)
            t[s[i]] = i

        return ret

'''
牵扯到连续子串的题，首先就要想到双指针，不过这个代码里的题解更骚一些，记录一下。
'''