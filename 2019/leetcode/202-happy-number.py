class Solution:
    def isHappy(self, n):
        """
        :type n: int
        :rtype: bool
        """
        if n == 1:
            return True
        while n > 0:
            print(n)
            s = 0
            while n > 0:
                unit = n % 10
                n = n // 10
                s += unit * unit
            n = s
            if n == 1:
                return True
            if n == 4:
                return False
        return False

if __name__ == "__main__":
    testCase = [19, 7, 0, 1]
    testCase = [7]
    for i in testCase:
        print(Solution().isHappy(i))