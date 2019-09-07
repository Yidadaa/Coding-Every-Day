class Solution:
    def numKLenSubstrNoRepeats(self, S: str, K: int) -> int:
        n = len(S)
        if n < K:
            return 0
        
        self.d = {}
        
        for x in S[0:K]:
            self.add(x)
        ret = int(len(self.d) == K)
        l = 0
        for x in S[K:]:
            self.add(x)
            self.remove(S[l])
            l += 1
            ret += int(len(self.d) == K)
        return ret
    
    def add(self, x):
        if x not in self.d:
            self.d[x] = 0
        self.d[x] += 1
        
    def remove(self, x):
        if self.d[x] == 1:
            del self.d[x]
        else:
            self.d[x] -= 1
