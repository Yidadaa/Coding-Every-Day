class Solution:
    """
    @param nums: A list of integers
    @return: The majority number occurs more than 1/3
    """
    def majorityNumber(self, nums):
        # 主元素问题，最经典的解法是消解法，由于其中一个数字个数是严格大于1/k的
        # 那么每取得k个不同的数字，就删除他们，那么剩下的数字肯定是主元素
        # 但是最简单粗暴的方法还是直接计数，时间复杂度o(n)，空间复杂度o(n-k)
        hashT = {}
        for i in nums:
            if i in hashT:
                hashT[i] += 1
                if hashT[i] >= float(len(nums)) / 3.0:
                    return i
            else:
                hashT[i] = 1

test = [[7,1,7,7,61,61,61,10,10,10,61],[1,2,3,4,4,4],[1,2,3,5,2,2,5,6,5,6,5],[99,2,99,2,99,3,3]]
print(list(map(lambda x:Solution().majorityNumber(x), test)))