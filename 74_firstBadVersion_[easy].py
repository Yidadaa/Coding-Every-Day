#class SVNRepo:
#    @classmethod
#    def isBadVersion(cls, id)
#        # Run unit tests to check whether verison `id` is a bad version
#        # return true if unit tests passed else false.
# You can use SVNRepo.isBadVersion(10) to check whether version 10 is a 
# bad version.
class Solution:
    """
    @param n: An integers.
    @return: An integer which is the first bad version.
    """
    def findFirstBadVersion(self, n):
        if n <= 0:
            return 0
        i = 0
        j = n
        lastM = 0
        while True:
            m = int((i + j) / 2)
            if m == lastM:
                break
            if self.isBadVersion(m) is False:
                i = m
            else:
                j = m
            lastM = m
        return m + 2

    def isBadVersion(self, n):
        testData = [False, False, False, True, True, True]
        if n < len(testData):
            return testData[n]
        else:
            return True

print(list(map(lambda x: Solution().findFirstBadVersion(x), [6])))