class Solution:
    def maxSideLength(self, mat: List[List[int]], threshold: int) -> int:
        self.m, self.n = len(mat), len(mat[0])
        self.s_mat = mat
        self.t = threshold
        
        for i in range(self.m):
            for j in range(self.n):
                for (x, y, cof) in [(i - 1, j, 1), (i, j - 1, 1), (i - 1, j - 1, -1)]:
                    if x >= 0 and x < self.m and y >= 0 and y < self.n:
                        self.s_mat[i][j] += cof * self.s_mat[x][y]
        
        l, r = 0, min(self.m, self.n)
        while l < r:
            m = (l + r) >> 1
            if not self.test(m): r = m
            else: l = m + 1
        return l - 1 if not self.test(l) and l > 0 else l

    def test(self, w):
        if w == 0: return True
        for i in range(self.m - w + 1):
            for j in range(self.n - w + 1):
                s = self.s_mat[i + w - 1][j + w - 1] + \
                    (self.s_mat[i - 1][j - 1] if i > 0 and j > 0 else 0) - \
                    (self.s_mat[i + w - 1][j - 1] if j > 0 else 0) - \
                    (self.s_mat[i - 1][j + w - 1] if i > 0 else 0)
                if s <= self.t:
                    return True
        return False
