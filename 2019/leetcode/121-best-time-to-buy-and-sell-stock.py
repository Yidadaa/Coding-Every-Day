class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if len(prices) < 1:
            return 0
        
        ret = 0
        minPrice = prices[0]
        
        for x in prices:
            minPrice = min(x, minPrice)
            ret = max(ret, x - minPrice)
            
        return ret
