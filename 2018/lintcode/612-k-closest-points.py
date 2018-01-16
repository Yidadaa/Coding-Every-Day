"""
k个最近的点
"""
"""
Definition for a point.
"""
class Point:
    def __init__(self, a=0, b=0):
        self.x = a
        self.y = b

import math

class Solution:
    """
    @param: points: a list of points
    @param: origin: a point
    @param: k: An integer
    @return: the k closest points
    """
    def kClosest(self, points, origin, k):
      # write your code here
      pointsWithDistance = []
      for p in points:
        pointsWithDistance.append({
          'd': math.sqrt(math.pow(p.x - origin.x, 2) + math.pow(p.y - origin.y, 2)),
          'point': p
        })
      pointsWithDistance = sorted(pointsWithDistance, key=lambda a: (a['d'], a['point'].x, a['point'].y))
      return [x['point'] for x in pointsWithDistance[0:k]]

if __name__ == '__main__':
  testClass = Solution()
  testCase = [[4,6],[4,7],[4,4],[2,5],[1,1]]
  points = [Point(x[0], x[1]) for x in testCase]
  res = testClass.kClosest(points, Point(0, 0), 3)
  print([[p.x, p.y] for p in res])