class Solution:
    def selfDividingNumbers(self, left: int, right: int) -> List[int]:
        ret = []
        for i in range(left, right + 1):
            if self.isSelfDivided(i):
                ret.append(i)
        return ret
        
    def isSelfDivided(self, num):
        _num = num
        ans = True
        while _num > 0:
            d = _num % 10
            if d == 0:
                return False
            ans = num % d == 0 and ans
            _num //= 10
        return ans
