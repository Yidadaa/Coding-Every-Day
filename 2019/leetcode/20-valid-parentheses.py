class Solution:
    def isValid(self, s: str) -> bool:
        d = {
            ')': '(',
            '}': '{',
            ']': '['
        }
        stack = []
        for c in s:
            if c not in d:
                stack.append(c)
            elif len(stack) == 0:
                return False
            elif stack[len(stack) - 1] == d[c]:
                stack.pop()
            else:
                return False
        return len(stack) == 0
