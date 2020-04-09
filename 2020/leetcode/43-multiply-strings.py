class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        ret = ''
        zeros = ''
        for i in range(len(num1)):
            m = self.mul(num2, num1[-i - 1])
            ret = self.add(m + zeros, ret)
            zeros += '0'
        return '0' if ret[0] == '0' else ret

    def mul(self, s, x):
        s = list(s)
        x = int(x)
        ret, res = '', 0
        while s or res > 0:
            a = int(s.pop()) if s else 0
            b = a * x + res
            res = b // 10
            ret = str(b % 10) + ret
        return ret

    def add(self, a, b):
        a = list(a)
        b = list(b)
        ret, res = '', 0
        while a or b or res:
            x = int(a.pop()) if a else 0
            y = int(b.pop()) if b else 0
            s = x + y + res
            res = s // 10
            ret = str(s % 10) + ret
        return ret

if __name__ == '__main__':
    print(Solution().multiply('123', '456'))