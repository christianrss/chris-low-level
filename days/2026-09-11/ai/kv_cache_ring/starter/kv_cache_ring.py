class KVRing:
    def __init__(self, cap):
        self.cap = cap
        self.buf = [None] * cap
        self.pos = 0
        self.count = 0
    def write(self, item):
        # TODO [D9-KV-WRITE]
        raise NotImplementedError
    def read(self, i):
        # TODO [D9-KV-READ]
        raise NotImplementedError
    def window(self):
        # TODO [D9-KV-WINDOW]
        raise NotImplementedError
