class Solution:
    def rangeBitwiseAnd(self, m: int, n: int) -> int:
        if m == 0 or m == n:
            return m
        c = 0
        while m != n:
            m >>= 1
            n >>= 1
            c += 1
        return m << c

    '''
    核心思想：n & (n - 1) 会使最低位二进制置0，如果n与m二进制不等长，那么结果必为0，只需要讲两者不断右移，剩余位填0即可
    '''
