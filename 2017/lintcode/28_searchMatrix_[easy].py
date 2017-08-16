class Solution:
    """
    @param: : matrix, a list of lists of integers
    @param: : An integer
    @return: a boolean, indicate whether matrix contains target
    """

    def searchMatrix(self, matrix, target):
        theArray = []
        isIn = False
        i = 0
        j = len(matrix)
        if j > 0:
            lastM = i
            m = j
            while True:
                m = int((i + j) / 2)
                if lastM == m:
                    break
                if matrix[m][0] > target:
                    j = m
                elif matrix[m][0] < target:
                    i = m
                else:
                    return True
                lastM = m
            if matrix[m][-1] < target and m < len(matrix) - 1:
                m += 1
            theArray = matrix[m]
            i = 0
            j = len(theArray)
            if j > 0:
                lastM = i
                m = j
                while True:
                    m = int((i + j) / 2)
                    if lastM == m:
                        break
                    if theArray[m] > target:
                        j = m
                    elif theArray[m] < target:
                        i = m
                    else:
                        return True
                    lastM = m
        return False


A = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 50], [53, 60, 64, 70]]
test = [[A, 1, True], [A, 2, False], [A, 3, True], [A, 50, True], [A, 11, True], [[], 0, False], [A, 70, True], [A, 53, True]]
print(list(map(lambda x: Solution().searchMatrix(x[0], x[1]) == x[-1], test)))
# print(Solution().searchMatrix([[1,5,8,12,13,15,18,20,25,26,28,33,38,40,43,49,52,53,59],[84,100,110,129,141,156,177,198,220,242,254,266,284,297,316,326,343,358,373],[388,398,419,439,449,460,472,495,516,539,560,582,600,610,624,643,668,691,710],[720,733,751,765,787,804,814,832,856,880,905,930,950,974,999,1012,1022,1039,1061],[1081,1091,1102,1126,1151,1175,1194,1219,1239,1253,1263,1274,1287,1298,1308,1318,1337,1361,1382],[1404,1417,1437,1452,1466,1487,1503,1518,1537,1555,1578,1590,1601,1613,1636,1659,1669,1688,1712]], 1888))