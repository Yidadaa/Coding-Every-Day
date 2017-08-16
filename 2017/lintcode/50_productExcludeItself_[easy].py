class Solution:
    """
    @param A: Given an integers array A
    @return: An integer array B and B[i]= A[0] * ... * A[i-1] * A[i+1] * ... * A[n-1]
    """
    def productExcludeItself(self, A):
        '''
        这道题说实话我只会写o(n^2)的算法，搜索之后才知道可以用数组来存储左积和右积
        '''
        length = len(A)
        if length == 1:
            return [1]
        LMs = []
        RMs = []
        leftMul = 1
        rightMul = 1
        B = []
        for i in range(length):
            rightMul *= A[length - 1 - i]
            leftMul *= A[i]
            LMs.append(leftMul)
            RMs.append(rightMul)
        for i in range(length):
            if i == 0:
                B.append(RMs[length - 2])
            elif i == length - 1:
                B.append(LMs[length - 2])
            else:
                B.append(RMs[length - i -2] * LMs[i - 1])
        return B

print(Solution().productExcludeItself([4, -1, 3]))