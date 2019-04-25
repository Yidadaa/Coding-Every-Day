class Solution:
    def isHappy(self, n: int) -> bool:
        # Write your code here
        src = set([n])
        tmp = None
        while n != 1:
            tmp = n
            s = 0
            while n > 0:
                s += (n % 10) ** 2
                n //= 10
            n = s
            if tmp == n or n in src:
                return False
            src.add(n)
        return True

'''
Tips:
1. 使用`set`加快查找速度
'''
