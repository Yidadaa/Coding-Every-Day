class Solution:
    # @param gas, a list of integers
    # @param cost, a list of integers
    # @return an integer
    def canCompleteCircuit(self, gas, cost):
        # 对于该序列，求gas[i] - cost[i]的序列A
        # 若存在符合条件的解，则有sum(A)>=0
        # 并且存在i<len(A)，使得A[i:]中的任意一个值均大于0,
        # 则i就是所求的解
        if sum(gas) < sum(cost):
            return -1
        tmp = 0
        start = 0
        for i in range(len(gas)):
            tmp = tmp + gas[i] - cost[i]
            if tmp < 0:
                start = i
        if tmp >= 0:
            start += 1
            while gas[start - 1] >= cost[start - 1] and start > 0:
                start -= 1
            return start
        else:
            return -1

test = [[[0], [0]], [[1, 1, 3, 1], [2, 2, 1, 1]], [[1,4,2,3,1], [2,2,1,1,5]]]
print(list(map(lambda x: Solution().canCompleteCircuit(x[0], x[1]), test)))