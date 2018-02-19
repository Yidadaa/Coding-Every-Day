"""
买卖股票的最佳时机 IV

这是一道动态规划的题目。
动态规划的求解，一般要找准以下要素：
1. 确定问题的状态空间，一般与问题需要求解的变量有关；
2. 确定问题的状态转移方程，这一步是最玄学的，每道题的转移方程都不一样，但是基本都跟时间或者操作有关；
3. 根据状态转移方程，遍历状态空间，得出最优解。

回到本题，每次买卖操作之后的总收益s，可以作为问题的状态，能够影响该状态（收益s）的，就是买入/卖出操作，
对于买入与卖出，有条件限制是k次以内，即只能进行不大于k次的买入与卖出操作，注意买入 + 卖出才算作一次操作
周期。

那么在第i天，我们进行的操作就有可能是第n次，其中 n > int(i / 2) 且 n <= k。
既然能够影响状态（收益s）的只能是买入与卖出操作，那么我们就可以使用两个 k 维的 buy 和 sell 数组来存储 s
的所有状态，即：
    buy[n] 表示进行第 n 次买入操作后的总收益;
    sell[n] 表示进行第 n 次卖出操作后的总收益;
并且有以下递推公式：
    buy[n] = max{ buy[n], sell[n - 1] - price[i] }
        即第 n 次买入操作的收益，等于第 n - 1 次卖出操作后的收益减去当天的股票价格；
    sell[n] = max{ sell[n], buy[n] + price[i] }
        即第 n 次卖出操作的收益，等于第 n 次买入操作后的收益加上当天的股票价格。
其中的 max 操作，保证了数组中所有的值都是当前状态下的最大值。

那么，对于第 i 天，我们只需要遍历所有的 n，然后按照以上递推公式更新 buy 和 sell 数组，
就可以得到当天之后，可以获得的收益的最大值。
当我们遍历完所有天数后，最后一次卖出操作后得到的收益，就是符合条件的最大收益。

注：这个代码在Lintcode上会超时，但是同样的算法换成C++版本的就不会超时，只能吐槽lintcode的超时判定很傻逼了。
"""

class Solution:
    """
    @param K: An integer
    @param prices: An integer array
    @return: Maximum profit
    """
    def maxProfit(self, K, prices):
        days = len(prices)
        if days == 0:
            return 0
        if K > days / 2:
            K = int(days / 2) + 1
        buy = [-prices[0] for i in range(K)]
        sell = [0 for i in range(K)]
        for i in range(days):
            buy[0] = max(buy[0], -prices[i]) # 注意，其中的 buy[0] 是第 i - 1 天的第一次买入收益
            sell[0] = max(sell[0], buy[0] + prices[i]) # 其中的 sell[0] 是第 i - 1 天的第一次卖出收益
            # 下面要对第 i 天的 buy 和 sell 进行更新
            # 由于 buy[j] 和 sell[j] 的更新依赖于第 i - 1 天的 buy[j - 1] 和 sell[j - 1]
            # 所以需要从 K - 1 往前遍历，如果从 0 遍历，buy[j - 1]会被覆盖掉
            for j in range(K - 1, 0, -1):
                buy[j] = max(buy[j], sell[j - 1] - prices[i])
                sell[j] = max(sell[j], buy[j] + prices[i])

        return sell[K - 1] # 直接返回最后一次卖出的收益，作为最大收益

if __name__ == '__main__':
    testClass = Solution()
    testCase = [4, 4, 6, 1, 1, 4, 2, 5]
    res = testClass.maxProfit(20000, testCase)
    print(res)