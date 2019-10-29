class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # 横向和纵向
        for i in range(9):
            if not self.check(board[i]): return False
            if not self.check([board[j][i] for j in range(9)]): return False
            
        # 检验格子
        for i in range(3):
            for j in range(3):
                block = []
                for k in range(3):
                    block += board[i * 3 + k][j * 3:(j + 1) * 3]
                if not self.check(block): return False
        return True
            
    def check(self, nums):
        count = [0] * 10
        for x in nums:
            if x is '.': continue
            x = int(x)
            if count[x] == 1: return False
            count[x] = 1
        return True
