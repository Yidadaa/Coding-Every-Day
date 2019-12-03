class Solution:
    def countSquares(self, matrix: List[List[int]]) -> int:
        s = matrix.copy()
        
        m, n = len(matrix), len(matrix[0])
        
        for i in range(m):
            for j in range(n):
                if i > 0: s[i][j] += s[i - 1][j]
                if j > 0: s[i][j] += s[i][j - 1]
                if i > 0 and j > 0: s[i][j] -= s[i - 1][j - 1]
                    
        ret = 0
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == 0: continue
                for w in range(min(m - i, n - j)):
                    sq = s[i + w][j + w]
                    if i > 0: sq -= s[i - 1][j + w]
                    if j > 0: sq -= s[i + w][j - 1]
                    if i > 0 and j > 0: sq += s[i - 1][j - 1]
                    if sq == (w + 1) * (w + 1): ret += 1
                    else: break
        return ret
