"""
恢复ip地址

没有什么技术含量，因为一个字符串的4块划分是有限的，直接穷举就行了
但是lintcode的判定特别傻逼，明明题目中说好了不用输出顺序问题，判定的时候还是要按它的顺序来，fxxk
"""

class Solution:
    """
    @param: s: the IP string
    @return: All possible valid IP addresses
    """
    def restoreIpAddresses(self, s):
        res = []
        for c in s:
            if c > '9' or c < '0':
                return []
        """
        划分字符串
        @param: n: number of pieces
        @param: str: string
        @return: [number]
        """
        def splitStr(n, s, last):
            if n == 1:
                if (len(s) == 1 or (len(s) > 1 and s[0] != '0')) and int(s) <= 255 and int(s) >= 0:
                    last.append(int(s))
                    ip = '.'.join(map(str, last))
                    if ip not in res:
                        res.append(ip)
            else:
                for i in range(3):
                    subs = s[0:i + 1]
                    if (len(subs) == 1 or (len(s) > 1 and subs[0] != '0')) and int(subs) <= 255 and int(subs) >= 0:
                        lastList = []
                        lastList.extend(last)
                        lastList.append(int(subs))
                        splitStr(n - 1, s[i + 1:], lastList)
        splitStr(4, s, [])
        return list(res)

if __name__ == '__main__':
    testClass = Solution()
    testCase = "121212"
    res = testClass.restoreIpAddresses(testCase)
    print(res)