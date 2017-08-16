class Solution:
    """
    @param A : An integer array
    @return : Two integer
    """
    def singleNumberIII(self, A):
        if len(A) < 2:
            res = []
            res.extend(A)
            res.extend([0 for i in range(2 - len(A))])
            return res
        dict_ = {}
        for i in A:
            if i in dict_:
                dict_[i] += 1
                if dict_[i] == 2:
                    del dict_[i]
            else:
                dict_[i] = 1
        return list(dict_.keys())

test = [[1,2,3,3,4,4],[1,2], [], [1]]
print(list(map(lambda x:Solution().singleNumberIII(x), test)))