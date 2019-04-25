class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        s_list = list(s)
        t_list = list(t)
        s_list.sort()
        t_list.sort()
        return s_list == t_list

'''
Tips:
1. 使用`collections`库可以提速
'''