    """
    矩阵归零

    常数级别的算法，用矩阵第一行列存储状态
    """

    class Solution:
        """
        @param: matrix: A lsit of lists of integers
        @return: 
        """
        def setZeroes(self, matrix):
            # 首先判断第一行列需不需要归零
            if len(matrix) == 0:
                return
            l1 = 0 in matrix[0]
            r1 = 0 in [x[0] for x in matrix]
            for i in range(1, len(matrix[0])):
                matrix[0][i] = 0 if 0 in [x[i] for x in matrix] else matrix[0][i]
            for i in range(1, len(matrix)):
                matrix[i][0] = 0 if 0 in matrix[i] else matrix[i][0]
            for i in range(1, len(matrix[0])):
                if matrix[0][i] == 0:
                    for j in range(1, len(matrix)):
                        matrix[j][i] = 0
            for i in range(1, len(matrix)):
                if matrix[i][0] == 0:
                    for j in range(1, len(matrix[0])):
                        matrix[i][j] = 0
            if l1:
                for i in range(len(matrix[0])):
                    matrix[0][i] = 0
            if r1:
                for i in range(len(matrix)):
                    matrix[i][0] = 0

    if __name__ == '__main__':
        testClass = Solution()
        testCase = [[1, 2, 3], [0, 1, 2], [1, 0, 1]]
        res = testClass.setZeroes(testCase)
        print(testCase)