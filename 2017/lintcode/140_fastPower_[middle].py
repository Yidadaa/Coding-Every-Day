class Solution:
    """
    @param a, b, n: 32bit integers
    @return: An integer
    """
    def fastPower(self, a, b, n):
        '''
        又是一道数学题，首先有个公式：
        --> a^n = (a*a)^(n/2) if n % 2 == 0
        --> a^n = a*(a*a)^(n/2) if n % 2 == 1
        所以可以有:
        --> a^n = a^(2^bin[0]*...*2^bin[i]) 其中, bin为n的二进制表示
        那么就可以把o(n)的时间缩短到o(log n)
        
        '''
        res = 1
        while n > 0:
            res = (res * a) % b if n % 2 == 1 else res
            a = (a**2) % b
            n = int(n / 2)
        return res % b

test = [[2, 12, 3], [123, 2, 4], [3, 7, 5], [31, 1, 0]]
print(list(map(lambda x: Solution().fastPower(x[0], x[1], x[2]) == x[0]**x[2] % x[1], test)))