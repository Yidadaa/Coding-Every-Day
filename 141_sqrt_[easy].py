class Solution:
    """
    @param x: An integer
    @return: The sqrt of x
    """
    def sqrt(self, x):
        i = 0
        j = x
        if x == 1:
            return 1
        while j - i > 1:
            m = int((i + j) / 2)
            if m * m > x:
                j = m
            else:
                i = m
        return i

print([Solution().sqrt(i) for i in range(10)])