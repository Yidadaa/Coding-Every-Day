class Solution:
    """
    @param matrix: A list of lists of integers
    @param target: An integer you want to search in matrix
    @return: An integer indicate the total occurrence of target in the given matrix
    """
    def searchMatrix(self, matrix, target):
        # write your code here
        maxLine = len(matrix)
        if maxLine == 0:
            return 0
        maxRow = len(matrix[0])
        if maxRow == 0:
            return 0
        count = 0
        for i in range(maxLine):
            if self.indexOfList(target, matrix[i]) > -1:
                count += 1
        return count

    def indexOfList(self, num, list):
        i = 0
        n = len(list) - 1
        j = n
        while j >= i:
            mid = int((i + j) / 2)
            if num < list[mid]:
                j = mid - 1
            elif num > list[mid]:
                i = mid + 1
            else:
                return mid
        return -1

if __name__ == '__main__':
    s = Solution()
    print(s.searchMatrix([[62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80],[63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81],[64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82],[65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83],[66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84],[67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85]], 81))