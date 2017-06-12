class Solution:
    """
    @param A: A positive integer which has N digits, A is a string.
    @param k: Remove k digits.
    @return: A string
    """
    def DeleteDigits(self, A, k):
        '''
        联系之前做过的一道题，如果把这串数字看做“数字山峰”
        数字的大小是山峰的高低，若想让最后的值最小
        那么山峰的前面部分一定是平缓的，所以我们要做的
        就是不断地消除前面的山峰，例如A = '1232123', k = 3
        就有：
                #       #
              # # #   # #
            # # # # # # #
            1 2 3 2 1 2 3
            ^^^^^^^^^^^^^
            | | | | |
            | 2 1 3 | <- 删除顺序
            |_______|
                |-这里有个山峰，从山顶开始往下删除
        删除的顺序是 3 - 2 - 2
        最后的结果是1123
        '''
        A = list(map(int, list(A)))
        while k > 0:
            i = 0
            while i < len(A) - 1 and A[i] <= A[i + 1]:
                i += 1
            if len(A) > 1:
                del A[i]
            k -= 1
        i = 0
        while i < len(A) - 1 and A[i] == 0:
            # 消除前置0
            i += 1
        return ''.join(map(str, A[i:]))

test = [['44000032', 3, '2'], ['12321', 2, '121'], ['123', 3, '1']]
print(list(map(lambda x: Solution().DeleteDigits(x[0], x[1]) == x[2], test)))