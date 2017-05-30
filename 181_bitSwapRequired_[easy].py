class Solution:
    """
    @param a, b: Two integer
    return: An integer
    """
    def bitSwapRequired(self, a, b):
        '''
        这题不难，但是很烦，python的二进制转换太naive了，负数的二进制居然是直接在前面加负号
        '''
        def int2bin(n):
            if n >= 0:
                return bin(n)[2:].zfill(32)
            else:
                n = -n
                n = bin(n)[2:].zfill(32)
                tmp = 1 # 进位
                s = 0
                res = ''
                for i in range(32):
                    # 先取反，后加一
                    num = int(n[31 - i])
                    num = 1 - num # 取反 
                    s = (s + num + tmp) % 2
                    tmp = int((s + num + tmp) / 2)
                    res = str(s) + res
                return res
        a = int2bin(a)
        b = int2bin(b)
        count = 0
        for i in range(32):
            tmp = 0 if a[i] == b[i] else 1
            count += tmp

        return count

test = [[1, -1], [2, 3], [1, 1]]
print(list(map(lambda x: Solution().bitSwapRequired(x[0], x[1]), test)))