class Solution:
    def fourSumCount(self, A: List[int], B: List[int], C: List[int], D: List[int]) -> int:
        d1 = self.count(A, B)
        d2 = self.count(C, D)
        print(d1, d2)
        res = 0
        for k in d1:
            if -k in d2:
                res += d1[k] * d2[-k]
                d1[k] = 0
                d2[-k] = 0
        return res
        
    def count(self, A, B):
        d = {}
        for x in A:
            for y in B:
                s = x + y
                if s in d:
                    d[s] += 1
                else:
                    d[s] = 1
        return d
