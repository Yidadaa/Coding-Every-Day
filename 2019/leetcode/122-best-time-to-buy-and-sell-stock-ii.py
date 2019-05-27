class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        ret = 0
        for i in range(len(prices) - 1):
            ret += max(0, prices[i + 1] - prices[i])
            
        return ret
