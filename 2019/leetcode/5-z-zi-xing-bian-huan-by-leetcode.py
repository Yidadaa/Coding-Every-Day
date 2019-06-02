class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1:
            return s
        
        N = len(s)
        t = 2 * (numRows - 1)
        ret = ''
        for i in range(numRows):
            r = 0
            while r < N:
                n1 = t * r - i
                n2 = i + t * r

                if n1 >= N and n2 >= N:
                    break
                    
                if n1 == n2:
                    ret += s[n1]  
                elif n2 - n1 == t:
                    if n2 < N and n2 > -1:
                        ret += s[n2]
                    else:
                        break
                else:
                    if n1 >= 0:
                        ret += s[n1]
                    if n2 < N:
                        ret += s[n2]

                r += 1
        return ret
