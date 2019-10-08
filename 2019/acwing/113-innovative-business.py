# Forward declaration of compare API.
# def compare(a, b):
# @param a, b int
# @return bool
# return bool means whether a is less than b.


class Solution(object):
    def specialSort(self, N):
        """
        :type N: int
        :rtype: List[int]
        """
        ret = [1]
        for i in range(2, N + 1):
            l, r = 0, len(ret) - 1
            while l < r:
                m = (l + r) >> 1
                if compare(ret[m], i):
                    l = m + 1
                else:
                    r = m
            if l == len(ret) - 1 and compare(ret[-1], i):
                l += 1
            ret = ret[0:l] + [i] + ret[l:]
        print(ret)

# 插入排序的变种
