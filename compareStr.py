class Solution:
    """
    @param A : A string includes Upper Case letters
    @param B : A string includes Upper Case letters
    @return :  if string A contains all of the characters in B return True else return False
    """
    def __init__(self):
        self.str = ''
    def compareStrings(self, A, B):
        # write your code here
        self.str = A
        def func(x):
            if x in self.str:
                self.str = self.str.replace(x, '', 1) # 删除一个字符
                return True
            else:
                return False
        return sum(map(func, B)) == len(B)

print(Solution().compareStrings('ABCD', 'ABC'))