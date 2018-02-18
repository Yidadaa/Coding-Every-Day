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
                maxProfit += p - minPrice
                minPrice = p
            else:
                minPrice = p
        return maxProfit


if __name__ == '__main__':
    testClass = Solution()
    testCase = [6, 1]
    res = testClass.maxProfit(testCase)
    print(res)