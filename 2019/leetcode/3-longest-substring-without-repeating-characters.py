class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        d = {}
        ret = 0
        x = 0
        for i in range(len(s)):
            if s[i] in d:
                x = max(d[s[i]], x)
            ret = max(ret, i - x + 1)
            d[s[i]] = i + 1
        return ret
        
 '''
 TIPS:
 1. 称每次出现重复字符时，重复字符前一次出现的点为断点，ret用于存储最长无重复字串的长度，x则表示上次断点出现的位置，则用max操作不断更新x和ret的值即可
 '''
