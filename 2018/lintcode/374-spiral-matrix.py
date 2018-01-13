"""
螺旋矩阵

问题描述：
    给定如下矩阵：
    [
        [ 1, 2, 3 ],
        [ 4, 5, 6 ],
        [ 7, 8, 9 ]
    ]
    应返回 [1,2,3,6,9,8,7,4,5]。
"""
class Solution:
    """
    @param: matrix: a matrix of m x n elements
    @return: an integer list
    """
    def spiralOrder(self, matrix):
        if len(matrix) == 0 or len(matrix[0]) == 0:
            return []
        lmax = len(matrix[0])
        lmin = -1
        rmax = len(matrix)
        rmin = -1

        x = 0
        y = 0

        passed = set()

        path = []

        """
        @param:　x, y　next position
        @return: weather position [x, y] could access or not
        """
        def couldAccess(x, y):
            key = '-'.join([str(x), str(y)])
            return (x > lmin) and (x < lmax) and (y > rmin) and (y < rmax) and (key not in passed)

        lastDirection = 0 # 方向分别是→↓←↑，分别对应0,1,2,3
        while True:
            path.append(matrix[y][x])
            passed.add('-'.join([str(x), str(y)]))
            nextStep = [
                [x + 1, y], [x, y + 1], [x - 1, y], [x, y - 1]
            ]
            hasNextStepToGo = False
            for i in range(4):
                nextStepDirection = (lastDirection + i) % 4
                step = nextStep[nextStepDirection]
                lastDirection = nextStepDirection
                if couldAccess(step[0], step[1]):
                    x = step[0]
                    y = step[1]
                    hasNextStepToGo = True
                    break
            if hasNextStepToGo:
                continue
            else:
                break
        
        return path

if __name__ == '__main__':
    testClass = Solution()
    testCase = [[1,2,3,4],[4,5,6,7],[7,8,9,10],[1,2,4,5]]
    print(testClass.spiralOrder(testCase))