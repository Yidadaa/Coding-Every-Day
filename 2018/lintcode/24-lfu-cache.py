"""
LFU缓存策略

（Least Frequently Used）算法根据数据的历史访问频率来淘汰数据，其核心思想是“如果数据过去被访问多次，那么将来被访问的频率也更高”。
"""

class LFUCache:
    """
    @param: capacity: An integer
    """
    def __init__(self, capacity):
        # do intialization if necessary
        self.capacity = capacity
        self.cache = {}
        self.t = 0 # 用作简单的时间计数

    """
    @param: key: An integer
    @param: value: An integer
    @return: nothing
    """
    def set(self, key, value):
        # write your code here
        self.t += 1

        if key in self.cache:
            self.cache[key] = {
                'count': self.cache[key]['count'] + 1,
                'value': value,
                't': self.t
            }
        else:
            if len(self.cache) >= self.capacity:
                # 删除队尾元素，淘汰规则是优先淘汰引用计数最小的，若引用计数相同，则淘汰最久未访问的那个
                items = list(self.cache.items())
                minCount = items[0][1]['count']
                # 先找出最小引用计数
                for item in items:
                    if item[1]['count'] < minCount:
                        minCount = item[1]['count']
                # 再找出最久未引用键值
                delKey = ''
                minT = items[0][1]['t']
                for item in items:
                    if item[1]['count'] == minCount and item[1]['t'] < minT:
                        delKey = item[0]
                        minT = item[1]['t']
                del self.cache[delKey]
            self.cache[key] = {
                'count': 0,
                'value': value,
                't': self.t
            }
    """
    @param: key: An integer
    @return: An integer
    """
    def get(self, key):
        # write your code here
        self.t += 1
        res = -1
        if key in self.cache:
            res = self.cache[key]['value']
            self.cache[key]['count'] += 1
            self.cache[key]['t'] = self.t
        print(res)
        return res

if __name__ == '__main__':
    testClass = LFUCache(3)
    testCase = []
    testClass.set(1, 10)
    testClass.set(2, 20)
    testClass.set(3, 30)
    testClass.get(1)
    testClass.set(1, 40)
    testClass.get(4)
    testClass.get(3)
    testClass.get(2)
    testClass.get(1)
    testClass.set(5, 50)
    testClass.get(1)
    testClass.get(2)
    testClass.get(3)
    testClass.get(4)
    testClass.get(5)