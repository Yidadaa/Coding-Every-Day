class Solution:
    def strStr(self, source, target):
        # write your code here
        if source == None or target == None:
            return -1
        length = len(target)
        for i in range(len(source) - length + 1):
            curStr = source[i:i + length]
            if curStr == target:
                return i
        return -1

print(Solution().strStr(None, 'dfd'))