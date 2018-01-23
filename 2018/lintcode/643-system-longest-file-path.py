"""
系统最长路径

"""

class Solution:
    """
    @param: input: an abstract file system
    @return: return the length of the longest absolute path to file
    """
    def lengthLongestPath(self, input):
      
        maxLength = 0

        inputs = input.split('\n')

        deepPath = {
          -1: 0
        } # 用来保存每层路径的父目录长度

        for line in inputs:
          trimLine = line.replace('\t', '')
          numberOfTab = len(line) - len(trimLine) # 计算文件深度
          splitLine = trimLine.split('.') # 判断是否是文件
          if len(splitLine) == 2 and len(splitLine[1]) > 0:
            # 如果是文件，记录最大文件长度
            fileNameLength = deepPath[numberOfTab - 1] + len(trimLine)
            maxLength = fileNameLength if fileNameLength > maxLength else maxLength
          else:
            # 保存文件夹长度
            deepPath[numberOfTab] = deepPath[numberOfTab - 1] + len(trimLine) + 1 # 把分隔符的长度也算上

        return maxLength

if __name__ == '__main__':
  testClass = Solution()
  testCase = 'dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2.ext'
  res = testClass.lengthLongestPath(testCase)
  print(res)