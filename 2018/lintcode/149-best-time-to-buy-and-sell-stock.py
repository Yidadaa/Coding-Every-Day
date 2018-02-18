class Solution:
    """
    @param prices: Given an integer array
    @return: Maximum profit
    """
    def maxProfit(self, prices):
        if len(prices) == 0:
            return 0
        minPrice = prices[0]
        maxProfit = 0
        for p in prices:
            if p > minPrice:
                maxProfit = p - minPrice if p - minPrice > maxProfit else maxProfit
            else:
                minPrice = p
        return maxProfit


if __name__ == '__main__':
    testClass = Solution()
    testCase = []
    res = testClass.maxProfit(testCase)
    print(res)