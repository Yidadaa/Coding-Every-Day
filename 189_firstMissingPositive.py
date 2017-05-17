class Solution:
    # @param A, a list of integers
    # @return an integer
    def firstMissingPositive(self, A):
        '''
        其实问题的核心是实现in函数，判断数字是否在数组中，
        但是python已经内置这个函数了。
        常规一点的方法是进行排序，构造一个搜索二叉树，左子节点总是小于右子节点，
        然后开始做中序遍历，这样其实就完成了一次排序。
        '''
        i = 1
        while i in A:
            i += 1
        return i