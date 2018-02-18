class Solution:
    """
    @param prices: Given an integer array
    @return: Maximum profit
    """
    def maxProfit(self, prices):
        N = len(prices)
        if N == 0:
            return 0

        minPrice = prices[0]
        maxProfit = 0
        ap = list(range(N)) # 存储前i天卖出的最大收益
        bp = list(range(N)) # 存储后N - i天卖出的最大收益
        for i in range(N):
            p = prices[i]
            if p > minPrice:
                maxProfit = p - minPrice if p - minPrice > maxProfit else maxProfit
                ap[i] = maxProfit
            else:
                minPrice = p
                ap[i] = maxProfit

        maxPrice = prices[-1]
        maxProfit = 0
        for i in range(N - 1, -1, -1):
            p = prices[i]
            if p < maxPrice:
                maxProfit = maxPrice - p if maxPrice - p > maxProfit else maxProfit
                bp[i] = maxProfit
            else:
                maxPrice = p
                bp[i] = maxProfit

        # 将第i天的前i天最大收益和后i天最大收益相加，即可得到两次交易的最大收益
        maxProfit = 0
        for i in range(N):
            profit = ap[i] + bp[i]
            maxProfit = profit if profit > maxProfit else maxProfit
        return maxProfit


if __name__ == '__main__':
    testClass = Solution()
    testCase =  [4,4,6]
    res = testClass.maxProfit(testCase)
    print(res)