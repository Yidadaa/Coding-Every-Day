class Solution:
    # @param strs: A list of strings
    # @return: The longest common prefix
    def longestCommonPrefix(self, strs):
        if len(strs) == 0:
            return ''
        minLen = min(map(lambda s: len(s), strs))
        LCP = ''
        for i in range(minLen):
            tmp = strs[0][i]
            if sum(map(lambda s: s[i] == tmp, strs)) == len(strs):
                LCP += tmp
        return LCP

print(Solution().longestCommonPrefix(['fsadf', 'fsa', 'fsb']))