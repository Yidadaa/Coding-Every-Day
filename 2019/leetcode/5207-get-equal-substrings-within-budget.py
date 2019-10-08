class Solution:
    def equalSubstring(self, s: str, t: str, maxCost: int) -> int:
        s = list(map(ord, s))
        t = list(map(ord, t))
        
        diff = [abs(x[0] - x[1]) for x in zip(s, t)]
        
        # 两指针法求满足条件的子数组
        N = len(diff)
        l, r = 0, 0
        ret, s = 0, diff[l]
        while r < N:
            if s <= maxCost:
                ret = max(ret, r - l + 1)
                r += 1
                s += diff[r % N]
            else:
                s -= diff[l % N]
                l += 1
        return ret
