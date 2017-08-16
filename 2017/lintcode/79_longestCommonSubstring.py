class Solution:
    # @param A, B: Two string.
    # @return: the length of the longest common substring.
    def longestCommonSubstring(self, A, B):
        '''
        解题思路：
        使用矩阵来标记两个字符串中的字符是否相同：
        比如：A="lintcode", B="leetcode"
          c o d e
        l 0 0 0 0
        e 0 0 0 1
        e 0 0 0 1
        t 0 0 0 0
        c 1 0 0 0
        o 0 1 0 0
        d 0 0 1 0
        e 0 0 0 1
        则矩阵中的对角线为1的部分就是最长子串
        '''
        lenA = len(A)
        lenB = len(B)
        if lenA * lenB == 0:
            return 0
        matrix = [[A[k] == B[i] for k in range(lenA)] for i in range(lenB)]
        for i in range(lenB):
            for k in range(lenA):
                if matrix[i][k]:
                    matrix[i][k] = 1
                    if i > 0 and k > 0:
                        matrix[i][k] += matrix[i - 1][k - 1]
                else:
                    matrix[i][k] = 0
        return max(map(lambda x: max(x), matrix))

print(Solution().longestCommonSubstring("www.lintcode.com code", "www.ninechapter.com code"))