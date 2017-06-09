class Solution:
    """
    @param A : an integer array
    @return : a integer
    """
    def singleNumber(self, A):
        # 这一题比较巧妙，利用一个数与自己异或等于零的性质来做
        if len(A) == 0:
            return 0
        res = A[0]
        for i in A[1:]:
            res = res ^ i
        return res

test = [[1], [1, 2, 2, 3, 3], [1, 2, 2], []]
print(list(map(lambda x: Solution().singleNumber(x), test)))