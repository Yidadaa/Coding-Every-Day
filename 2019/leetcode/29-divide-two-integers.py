class Solution:
    def divide(self, dividend: int, divisor: int) -> int:
        max_ret = (1 << 31) - 1

        is_neg = -1 if dividend * divisor < 0 else 1
        dividend = -dividend if dividend < 0 else dividend
        divisor = -divisor if divisor < 0 else divisor

        l, r = 1, dividend
        while l < r:
            m = (l + r) >> 1
            if self.fast_mul(m, divisor) >= dividend: r = m
            else: l = m + 1

        if self.fast_mul(l, divisor) > dividend:
            l -= 1
        return min(max_ret, l * is_neg)

    def fast_mul(self, x, y):
        s = 0
        left_shift = 0
        while y > 0:
            if y & 1 == 1:
                s += x << left_shift
            left_shift += 1
            y >>= 1
        return s
