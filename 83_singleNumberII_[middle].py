class Solution:
    """
	@param A : An integer array
	@return : An integer
    """
    def singleNumberII(self, A):
        # 自己想的解法，比较无脑，就是用一个字典存储已经遍历的数组
        dict_ = {}
        if len(A) == 0:
            return 0
        for i in A:
            if i in dict_:
                dict_[i] += 1
                if dict_[i] == 3:
                    del dict_[i]
            else:
                dict_[i] = 1
        return list(dict_.keys())[0]

    def singleNumberII_2(self, A):
        # 大佬们的解法，用位运算的方法，先把整数用二进制表示
        # 如果某个数出现三次，则该数位上每个位都能被３整除，于是只需对结果进行
        # 取余操作即可
        # 例：a=4, bin(a)="100"
        # 三个a就是"300"，对３取余即可
        # python位操作比较繁琐，就不实现了
test = [[1,1,1,2], [0]]
print(list(map(lambda x:Solution().singleNumberII(x), test)))