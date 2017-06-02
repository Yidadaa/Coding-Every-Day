class Binary():
    '''
    32bit二进制类，包含一系列工具函数
    @param {Number} n - 接受一个整数
    '''
    def __init__(self, n = 0):
        self.bits = 32 # bit位数
        self.int = n
        self.bin = self.int2bin_32bit(n)
        self.neg = self.bin_neg(self.bin)

    def int2bin_32bit(self, n):
        # 将整数转换为32bit二进制字符串
        if n > 2**self.bits - 1 or n < -2**self.bits:
            # 溢出
            n = None
        elif n >= 0:
            n = bin(n)[2:].zfill(self.bits)
        else:
            n = bin(-n)[2:].zfill(self.bits) # 有符号二进制数的负数，用对应正数的取反后加一来表示
            n = self.bin_neg(n)
            n = self.bin_add(n, '1')
        return n

    def bin_neg(self, bin):
        # 二进制取反
        bin = bin.zfill(self.bits)
        neg_bin = ''
        for i in range(self.bits):
            bit = bin[i]
            neg_bin += str(1 - int(bit))
        return neg_bin

    def bin_add(self, bin_a, bin_b):
        # 二进制加法
        bin_a = bin_a.zfill(self.bits)
        bin_b = bin_b.zfill(self.bits)
        carry = 0
        bin_sum = ''
        for i in range(self.bits - 1, -1, -1):
            s = int(bin_a[i]) + int(bin_b[i]) + carry
            carry = int(s / 2) # 计算进位
            sum = s % 2 # 计算本位和
            bin_sum = str(sum) + bin_sum
        return bin_sum

    def bin2int_32bit(self, bin):
        # 二进制转整数
        bin = bin.zfill(self.bits) # 这里按32位进行转换
        integer = 0
        if bin[0] == '1':
            # 负数，先取反，后加一
            integer = -int(self.bin_add(self.bin_neg(bin), '1'), 2)
        else:
            integer = int(bin, 2)
        return integer

    def bit_and(self, bin_a, bin_b):
        # 与操作
        bin_a = bin_a.zfill(self.bits)
        bin_b = bin_b.zfill(self.bits)
        and_s = ''
        for i in range(self.bits):
            and_s += str(int(bin_a[i]) & int(bin_b[i])) # 按位与
        return and_s

class Solution:
    #@param n, m: Two integer
    #@param i, j: Two bit positions
    #return: An integer
    def updateBits(self, n, m, i, j):
        tpt = Binary(2**32 - 1 - 2**(j + 1) + 2**i).bin
        n_bin = Binary(n).bin
        m_bin = Binary(m << i).bin
        tpt_and_n_bin = Binary().bit_and(tpt, n_bin)
        res = Binary().bin_add(tpt_and_n_bin, m_bin)
        res_int = Binary().bin2int_32bit(res)
        return res_int

test = [[21, 214, 0, 9, 214], [-21, 214, 0, 9, -810], [1, -1, 0, 31, -1], [21, -1, 0, 31, -1], [456,31,27,31,-134217272], [456,31,26,31,2080375240]]
# test = [[-21, 214, 0, 9, -810]]
print(list(map(lambda x: Solution().updateBits(x[0], x[1], x[2], x[3]) == x[4], test)))


def test():
    # 测试用例
    if Binary(123).int2bin_32bit(123) == bin(123)[2:].zfill(Binary().bits):
        print('fun int2bin_32bit ok!')
    if Binary(1).bin_neg('10001') == ''.zfill(Binary().bits - 5).replace('0', '1') + '01110':
        print('fun bin_neg ok!')
    if Binary(1).bin_add('10', '11') == '101'.zfill(Binary().bits):
        print('fun bin_add ok!')
    if Binary(2).bin2int_32bit(Binary().int2bin_32bit(-23)) == -23:
        print('fun bin2int_32bit ok!') 

# test()