class Solution:
    # @param {string} s a string which consists of lowercase or uppercase letters
    # @return {int} the length of the longest palindromes that can be built
    def longestPalindrome(self, s):
        # Write your code here
        hashDict = {}
        oddStr = 0
        resLen = 0
        for i in s:
            hashDict[i] = 0
        for i in s:
            hashDict[i] += 1
        for i in hashDict.keys():
            v = hashDict[i]
            if v % 2 == 1:
                # 出现了奇数次
                oddStr = 1
            if v >= 2:
                # 出现了两次以上
                resLen += v - v % 2 # 统计出现了两次以上的字符个数
        return int(resLen + oddStr)

print(Solution().longestPalindrome('fasfsdf'))