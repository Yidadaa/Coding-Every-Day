class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        return self._generateParenthesis(n, n, '')
        
    def _generateParenthesis(self, l, r, prefix):
        lc = []
        rc = []
        if l == 0 and r == 0:
            return [prefix]
        if l > 0:
            lc = self._generateParenthesis(l - 1, r, prefix + '(')
        if r > 0 and r > l:
            rc = self._generateParenthesis(l, r - 1, prefix + ')')
            
        return lc + rc
