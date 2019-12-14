class CombinationIterator:

    def __init__(self, characters: str, combinationLength: int):
        self.chars = list(characters)
        self.n = combinationLength
        self.queue = [c for c in self.chars]
        self.q = [] if self.n > 1 else [c for c in self.chars]
        
    def gen(self):
        while len(self.queue) > 0 and len(self.q) == 0:
            s = self.queue.pop(0)
            for c in self.chars:
                if c <= s[-1]: continue
                if len(s) + 1 < self.n: self.queue.append(s + c)
                elif len(s) + 1 == self.n: self.q.append(s + c)

    def next(self) -> str:
        self.gen()
        if len(self.q) > 0: return self.q.pop(0)

    def hasNext(self) -> bool:
        self.gen()
        return len(self.q) > 0


# Your CombinationIterator object will be instantiated and called as such:
# obj = CombinationIterator(characters, combinationLength)
# param_1 = obj.next()
# param_2 = obj.hasNext()