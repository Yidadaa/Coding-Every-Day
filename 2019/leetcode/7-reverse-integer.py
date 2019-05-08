class Solution:
    def reverse(self, x: int) -> int:
        flag = x < 0
        x = abs(x)
        ret = 0
        while x > 0:
            ret = ret * 10 + x % 10
            x = x // 10
        if ret >= 2 << 30:
            return 0
        return -ret if flag else ret
