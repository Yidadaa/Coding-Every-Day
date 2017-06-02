class Solution:
    # @paramn n: An integer
    # @return: An integer
    # 卡特兰数，很神奇的东西
    def numTrees(self, n):
        if n <= 0:
            return 1
        return self.factorial(2 * n) / self.factorial(n + 1) / self.factorial(n)
        
    def factorial(self, n):
        s = 1
        while n > 1:
            s *= n
            n -= 1
        return s