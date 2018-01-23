"""
硬币问题II

最容易想的往往是使用递归完成，然而递归不仅耗时而且耗力
这是一道动态规划题，然而看了半天愣是没看懂……
详解：http://www.cnblogs.com/little-YTMM/p/5372680.html
动态规划具体的思想就是利用递推公式，将当前待求解问题转化为多个退化问题，
一直将其转化为初始问题，初始问题往往有最为简单的形式，这时只要反推即可求解。
对于本题来说，比较难理解的就是：
d(coins[0:i], amount) = d(coins[0:i-1, amount]) + d(coins[0:i], amount - coins[i])
这个公式的作用就是令coins和amount不断退化，直至退化为d([], 0) = 1
"""

class Solution:
    """
    @param amount: a total amount of money amount
    @param coins: the denomination of each coin
    @return: the number of combinations that make up the amount
    """
    def change(self, amount, coins):
        # write your code here
        s = {}
        s[0] = 1
        for c in coins:
            for i in range(c, amount + 1):
                if i in s:
                    s[i] = s[i] + s[i - c] if i - c in s else s[i]
                else:
                    s[i] = s[i - c] if i - c in s else 0

        return s[amount]

if __name__ == '__main__':
    testClass = Solution()
    testCase = []
    res = testClass.change(1000, [2, 3, 8])
    print(res)