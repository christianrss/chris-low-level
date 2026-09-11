class KVRing:
    def __init__(self, cap):
        self.cap = cap
        self.buf = [None] * cap
        self.pos = 0
        self.count = 0
    def write(self, item):
        # PEDAGOGY-SOLUTION: D9-KV-WRITE
        self.buf[self.pos] = item
        self.pos = (self.pos + 1) % self.cap
        self.count = min(self.cap, self.count + 1)
    def read(self, i):
        # PEDAGOGY-SOLUTION: D9-KV-READ
        if i < 0 or i >= self.count:
            raise IndexError(i)
        start = (self.pos - self.count) % self.cap
        return self.buf[(start + i) % self.cap]
    def window(self):
        # PEDAGOGY-SOLUTION: D9-KV-WINDOW
        return [self.read(i) for i in range(self.count)]
