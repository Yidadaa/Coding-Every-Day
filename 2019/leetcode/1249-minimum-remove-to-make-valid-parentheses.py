class Solution:
    def minRemoveToMakeValid(self, s: str) -> str:
        stack = []
        ret = list(s)
        
        for i in range(len(s)):
            c = s[i]
            if c not in ['(', ')']: continue
            if c == ')' and len(stack) > 0 and stack[-1][0] == '(':
                stack.pop()
            else:
                stack.append((c, i))
        for _, i in stack:
            ret[i] = ''
            
        ret = ''.join(ret)
        return ret