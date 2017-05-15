class Solution:
    # @param str: a string
    # @return an integer
    def atoi(self, str):
        # 很多边界条件，很烦
        isNeg = False
        resArr = []
        res = 0
        str = str.strip()
        if len(str) == 0:
            return 0
        if str[0] == '-':
            isNeg = True
            str = str[1:]
        elif str[0] == '+':
            isNeg = False
            str = str[1:]
        for i in str:
            if i <= '9' and i >= '0':
                resArr.append(i)
            else:
                break
        intLen = len(resArr)
        for i in range(intLen):
            res += (ord(resArr[i]) - 48) * pow(10, intLen - 1 - i)
        if isNeg:
            res = -res
        else:
            res = res
        if res > 2147483647:
            res = 2147483647
        if res < -2147483648:
            res = -2147483648
        return res

print(Solution().atoi('-2147483649'))