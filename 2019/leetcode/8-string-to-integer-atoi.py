class Solution:
    def myAtoi(self, str: str) -> int:
        i = 0
        N = len(str)
        # 跳过空白字符
        while i < N and str[i] == ' ':
            i += 1
        # 处理正负号
        flag = False
        if i < N and str[i] in ['-', '+']:
            flag = str[i] == '-'
            i += 1
        # 转换数字
        ret = 0
        while i < N and str[i] <= '9' and str[i] >= '0':
            ret = ret * 10 + int(str[i])
            i += 1
        # 处理溢出
        INT_MAX = 2 << 30
        if ret >= INT_MAX:
            ret = INT_MAX if flag else INT_MAX - 1
        return -ret if flag else ret
