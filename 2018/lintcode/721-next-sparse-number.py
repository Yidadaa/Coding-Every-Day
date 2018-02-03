"""
lintcode有毒，同样一段代码，C++可以过，python就TLE，shit
"""

class Solution:
    """
    @param: : a number
    @return: return the next sparse number behind x
    """

    def nextSparseNum(self, x):
        while (x >> 1) & x:
            x += 1
        return x

if __name__ == '__main__':
    testClass = Solution()
    testCase = [6, 4, 38, 0, -1, 341381939, 372228240]
    res = map(testClass.nextSparseNum, testCase)
    print(list(res))
