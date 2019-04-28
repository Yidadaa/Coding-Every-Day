class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        ret = -1
        if len(strs) == 0:
            return ''
        if len(strs) == 1:
            return strs[0]
        for i in range(len(strs[0])):
            for j in range(1, len(strs)):
                if i >= len(strs[j]) or strs[0][i] != strs[j][i]:
                    return strs[0][0:ret + 1]
            ret = i
        return strs[0][0:ret + 1]
