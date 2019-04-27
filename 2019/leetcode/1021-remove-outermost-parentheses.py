class Solution:
    def removeOuterParentheses(self, S: str) -> str:
        stack = []
        ret = ''
        for c in S:
            if not (c == '(' and len(stack) == 0 or c == ')' and len(stack) == 1):
                ret += c
            if c == '(':
                stack.append(c)
            else:
                stack.pop()
        return ret
