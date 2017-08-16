class Solution:
    # @param A, a list of integers
    # @return a boolean
    def canJump(self, A):
        # 这题其实很简单，只需要把前n步能到达的最大距离保存下来，遇到0时判断是否能跳过
        # 到结尾时用最大距离来判断能否到达结尾
        maxIndex = 0
        for i in range(len(A)):
            tmp = i + A[i]
            maxIndex = tmp if tmp > maxIndex else maxIndex
            if A[i] == 0 and maxIndex <= i and i < len(A) - 1:
                return False

        if maxIndex >= len(A) - 1:
            return True
        else:
            return False

test = [[2,3,1,1,9], [3,2,1,0,4], [1,2,1,0]]
print(list(map(lambda x: Solution().canJump(x), test)))