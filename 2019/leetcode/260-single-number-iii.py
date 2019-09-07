class Solution:
    def singleNumber(self, nums):
        pre = 0
        for x in nums:
            pre ^= x

        d = 0
        while pre != 0 and pre & 1 == 0:
            d += 1
            pre >>= 1

        ans = [0, 0]
        for x in nums:
            ans[(x >> d) & 1] ^= x
        return ans

'''
这道题的位运算解法堪称绝妙，首先对所有数进行异或运算，得到pre，然后找到pre中的非0位，
比如低d位，这意味着我们要找的两个数字a和b的低d位一定是一个为0，一个为1，那么只需要把
原数组按第d位为0或者为1分为两类即可，这样a和b肯定不在同一类，然后分别异或就完事儿了，牛逼
'''

if __name__ == "__main__":
    Solution().singleNumber([1, 1, 2, 2, 3, 4])