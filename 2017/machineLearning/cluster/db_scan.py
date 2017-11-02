'''
DB scan算法
'''
import math
from k_means import computeDistance

class Point():
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id

class DB():
    def __init__(self, points):
        self.points = points
        self.db = self.get_db()

    def get_db(self):
        n = len(self.points)
        db = [list(range(n)) for i in range(n)] # 用一个n*n的矩阵存储每两点之间的距离
        for i in range(len(self.points)):
            for j in range(len(self.points)):
                db[i][j] = computeDistance(self.points[i], self.points[j])
        return db

    def query(self, id1, id2):
        return self.db[id1][id2]


def db_scan(file_name = 'data'):

    data = []

    with open(file_name) as f:
        data = f.readlines()
        data = map(lambda x: list(map(float, x.split(' '))), data)
        data = list(data)

    db = DB(data)
    

if __name__ == '__main__':
    db_scan()