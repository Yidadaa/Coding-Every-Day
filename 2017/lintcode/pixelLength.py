import math
class Solution:
    '''给定一条线段的两端坐标，其中一端是原点，求被坐标系单位长度网格分割后的线段各段长度。
    '''
    def pixelLength(self, x, y):
        x = abs(x)
        y = abs(y)
        xAxis = list(range(int(x) + 1))
        xAxis.append(x)
        yAxis = list(range(int(y) + 1))
        yAxis.append(y)
        pixels = []
        if x == 0:
            pixels = list(map(lambda y: [0, y], yAxis))
        elif y == 0:
            pixels = list(map(lambda x: [x, 0], xAxis))
        else:
            k = y / x
            pixels.extend(map(lambda x: [x, k * x], xAxis))
            pixels.extend(map(lambda y: [y / k, y], yAxis))
            pixels = sorted(pixels, key=lambda a: a[0])
        resLength = []
        for i in range(len(pixels)):
            if i < len(pixels) - 1:
                p1 = pixels[i]
                p2 = pixels[i + 1]
                length = math.sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))
                if length > 0:
                    resLength.append(length)
        return resLength

print(Solution().pixelLength(3.4, 4.5))