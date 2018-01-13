class Solution:
    """
    @param: board: the board
    @return: whether the Sudoku is valid
    """
    def isValidSudoku(self, board):
        '''
        没什么难度，基本就是常数级复杂度
        比较绕的地方就是取数独块的时候
        '''
        board = [''.join(line) for line in board]

        isValid = True

        # 先测试行
        isValid = isValid and (sum([self.isDuplicatedArray(line) for line in board]) == 0)
    
        # 再测试列
        rows = [''.join([line[i] for line in board]) for i in range(9)] # 取出每一列
        isValid = isValid and (sum([self.isDuplicatedArray(row) for row in rows]) == 0)

        # 再测试九宫格
        for li in range(3):
            lines = board[li * 3 : (li + 1) * 3]
            for ri in range(3):
                block = ''.join([shortLine[ri * 3 : (ri + 1) * 3] for shortLine in lines])
                isValid = isValid and not self.isDuplicatedArray(block)

        return isValid

    '''
    判断一个数组是否包含重复元素
    @param: string: str array
    @return: whether the array is duplicated
    '''
    def isDuplicatedArray(self, string):
        string = ''.join(string) if type(string) == list else string
        string = string.replace('.', '') # 过滤掉填充符
        return len(string) != len(set(string))

if __name__ == '__main__':
    testClass = Solution()
    testCase = [".87654321","2........","3........","4........","5........","6........","7........","8........","9........"]
    print(testClass.isValidSudoku(testCase))