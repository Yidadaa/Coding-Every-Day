class Solution:
    """
    @param nums: A list of integers
    @return: A list of integers includes the index of the first number 
             and the index of the last number
    """
    def subarraySumClosest(self, nums):
        '''
        这道题和138是类似的，不过牵扯到求最小差，就比较麻烦了
        首先按照138的方法，根据公式：
        # 若sum(0, i) = sum(0, j)，则sum(i+1, j) = 0。
        将前n项和给求出来，放进hash表，在这个过程中，一旦发现
        有sum==0或者sum1==sum2的，就将其视为最终解并返回。
        放进hash表后，将表的键从小到大排列，并求相邻两项之间
        的差，求出差值最小的两项(m,n)，通过反查hash表，可以
        得到和为m,n的下标值i,k，则(i+1,k)为最终解。
        此外，将o(n^2)复杂度下降到o(nlogn)的方法，一般是排序
        和二分。
        '''
        length = len(nums)
        if length < 2:
            return [0, 0]
        s = 0
        res = {}
        for i in range(length):
            s += nums[i]
            if s == 0:
                return [0, i]
            if s in res:
                return [res[s] + 1, i]
            else:
                res[s] = i
        arr = list(res.keys())
        arr.sort()
        minDiff = abs(arr[0])
        index = [0, res[arr[0]]]
        for i in range(len(arr) - 1):
            diff = abs(arr[i] - arr[i + 1]) 
            if diff < minDiff:
                index = [res[arr[i]], res[arr[i + 1]]]
                index.sort()
                index[0] += 1
                minDiff = diff
        index.sort()
        return index

print(Solution().subarraySumClosest([-3,1,1,-3,5]))