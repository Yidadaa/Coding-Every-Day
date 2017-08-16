class Solution:
    """
    @param numbers: Give an array numbers of n integer
    @param target : An integer
    @return : return the sum of the three integers, the sum closest target.
    """
    def threeSumClosest(self, numbers, target):
        '''
        这一题是求最接近target的三数之和，与57号题很相似，但是细节上有所区分。
        还是利用两指针法遍历排序数组，根据当前遍历的三元组之和与target的差来判断
        lo和hi的步进，如果差为正，则步进hi，使三元组的和变小；如果差为负，则步进
        lo，使三元组之和变大；如果差为0，则当前三元组为最优解之一，直接返回。
        '''
        if len(numbers) < 3:
            return None
        numbers.sort()
        res = {}
        for i in range(len(numbers) - 2 ):
            if i == 0 or (i > 0 and numbers[i] != numbers[i - 1]):
                lo = i + 1
                hi = len(numbers) - 1
                s = numbers[i] + numbers[lo] + numbers[hi]
                minDiff = s - target
                res[abs(minDiff)] = s
                while lo < hi:
                    s = numbers[i] + numbers[lo] + numbers[hi]
                    diff = s - target
                    if diff == 0:
                        return target
                    if abs(diff) < abs(minDiff):
                        minDiff = diff
                        res[abs(diff)] = s
                    if diff < 0:
                        while lo < hi and numbers[lo] == numbers[lo + 1]:
                            lo += 1
                        lo += 1
                    else:
                        while lo < hi and numbers[hi] == numbers[hi - 1]:
                            hi -= 1
                        hi -= 1
        return res[min(res)]

print(Solution().threeSumClosest([1,2,3], 20))