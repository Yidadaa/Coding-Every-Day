class Solution:
    #@param n: Given a decimal number that is passed in as a string
    #@return: A string
    def binaryRepresentation(self, n):
        '''
        这道题的测试用例很愚蠢，而且我也不知道为什么这道题通过率只有19%
        '''
        if len(n) < 1:
            return ''
        flag = True if n[0] == '-' else False # 是否为负数
        n = n[1:] if flag else n # 取正
        n = n.split('.')
        int_part = int(n[0])
        dec_part = n[1]
        int_part = bin(int_part)[2:] # 整数部分转换为二进制
        dec_part = self.dec2bin(dec_part) # 小数部分转换为二进制
        if dec_part is False:
            return 'ERROR'
        res = int_part if dec_part == '' else int_part + '.' + dec_part
        res = '-' + res if flag is True else res
        return res

    def dec2bin(self, dec):
        dec = float('0.' + dec)
        if dec == 0.0:
            return ''
        bits = []
        length = 0
        while length < 32 and dec != 0.0:
            dec *= 2
            bit = '1' if dec >= 1 else '0' # 获得比特位
            bits.append(bit)
            dec = dec - 1 if dec >= 1 else dec # 减去整数部分
            length += 1
        if length == 32 and dec != 0.0:
            # 小数部分无法精确表示
            return False
        return ''.join(bits)

test = [['3.72', 'ERROR'], ['1.5', '1.1'], ['3.5', '11.1'], ['-3.5', '-11.1'], ['1.0', '1']]
print(list(map(lambda x: Solution().binaryRepresentation(x[0]) == x[1], test)))