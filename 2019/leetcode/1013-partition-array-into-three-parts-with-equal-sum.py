class Solution:
    def canThreePartsEqualSum(self, A: List[int]) -> bool:
        s_A = sum(A)
        if s_A % 3 != 0:
            return False
        
        s, count, avg = 0, 0, s_A // 3
        
        for x in A:
            s += x
            if s == avg:
                count += 1
                s = 0
            if count == 2:
                return True
            
        return False
