class Solution:
    # @param {TreeNode} root the root of binary tree
    # @return {TreeNode} the max node
    '''
    其实就是遍历二叉树
    '''
            
    def preOrder(self, node):
        maxNode = node
        if node == None:
            return
        leftMax = self.preOrder(node.left)
        rightMax = self.preOrder(node.right)
        for i in [node, leftMax, rightMax]:
            if i != None and i.val > maxNode.val:
                maxNode = i
        return maxNode
        
    def maxNode(self, root):
        # Write your code here
        return self.preOrder(root)