class Solution:
    """
    @param: : a number
    @return: return the next sparse number behind x
    """

    def nextSparseNum(self, x):
        """
        判断是否是稀疏数
        """
        def isSparseNum(n):
            last = False
            while n != 0:
                cur = ((n >> 1) & 1)
                if cur and last:
                    return False
                last = cur
                n = n >> 1
            return True
        
        while not isSparseNum(x):
            x += 1
        return x

if __name__ == '__main__':
    testClass = Solution()
    testCase = [6, 4, 38, 0, -1, 341381939]
    res = map(testClass.nextSparseNum, testCase)
    print(list(res))