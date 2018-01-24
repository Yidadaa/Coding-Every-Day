class Solution:
    
    """
    @param: nums1: an integer array
    @param: nums2: an integer array
    @return: an integer array
    """
    def intersection(self, nums1, nums2):
        array1 = set(nums1)
        array2 = set(nums2)
        if len(array2) < len(array1):
            # 让array1始终是较短的那个
            [array1, array2] = [array2, array1]
        res = []
        for n in array1:
            if n in array2:
                res.append(n)
        return res

if __name__ == '__main__':
    testClass = Solution()
    testCase = [[1, 2, 3], [1, 2, 4]]
    res = testClass.intersection(testCase[0], testCase[1])
    print(res)