class Solution:
    def numUniqueEmails(self, emails: List[str]) -> int:
        s = set()
        for e in emails:
            prefix = ''
            suffix = ''
            for i in range(len(e)):
                if e[i] == '+':
                    while e[i] != '@':
                        i += 1
                if e[i] == '@':
                    suffix = e[i + 1:]
                    break
                elif e[i] != '.':
                    prefix += e[i]
            s.add(prefix + '@' + suffix)
        return len(s)
        
'''
用python的split函数很简单，但是手写更考验算法功底
'''
