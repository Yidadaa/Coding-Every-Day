class Solution:
    def balancedString(self, s: str) -> int:
        if len(s) == 0: return 0
        
        count = self.count(s)
        avg = len(s) // 4
        sub_count = {k: count[k] - avg for k in count}
        
        ret = 0
        if any([x != 0 for x in sub_count.values()]):
            # 二分法求解
            neg, pos = {}, {}
            for k, v in sub_count.items():
                if v < 0: neg[k] = v
                elif v > 0: pos[k] = v
            
            l, r = 1, len(s)
            while l < r:
                m = (l + r) >> 1
                if self.test(s, m, neg, pos): r = m
                else: l = m + 1
            ret = l
            
        return ret
        
    def test(self, s:str, k:int, neg:dict, pos:dict):
        l = -1
        count = self.count(s[0:k - 1])
        for r in range(k - 1, len(s)):
            if l >= 0:
                count[s[l]] = max(0, count[s[l]] - 1)
            count[s[r]] += 1
            l += 1
            if all([count[key] >= pos[key] for key in pos]): return True

        return False
    
    def count(self, s:str):
        count = {k: 0 for k in 'QWER'}
        for c in s: count[c] += 1
        return count

if __name__ == '__main__':
    Solution().balancedString("QQWE")