class ProductOfNumbers:

    def __init__(self):
        self.q = []
        self.m = []
        self.count = 0
        self.n = 200

    def add(self, num: int) -> None:
        st, ed = len(self.q) - self.count, len(self.q)
        for i in range(st, ed):
            self.m[i] *= num
        self.count = (self.count + 1) % self.n
        self.q.append(num)
        self.m.append(num)

    def getProduct(self, k: int) -> int:
        ret = self.m[-k]
        for i in range(self.count, k, self.n):
            if i == 0: continue
            ret *= self.m[-i]
        return ret