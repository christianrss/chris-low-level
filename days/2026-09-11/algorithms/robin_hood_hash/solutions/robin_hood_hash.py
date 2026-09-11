class RobinHood:
    def __init__(self, cap=8):
        self.cap = cap
        self.keys = [None] * cap
        self.dist = [-1] * cap
    def _probe(self, key):
        # PEDAGOGY-SOLUTION: D9-RH-PROBE
        return hash(key) % self.cap
    def insert(self, key):
        # PEDAGOGY-SOLUTION: D9-RH-INSERT
        idx = self._probe(key)
        d = 0
        while True:
            if self.keys[idx] is None:
                self.keys[idx] = key
                self.dist[idx] = d
                return idx
            if self.keys[idx] == key:
                return idx
            if self.dist[idx] < d:
                self.keys[idx], key = key, self.keys[idx]
                self.dist[idx], d = d, self.dist[idx]
            idx = (idx + 1) % self.cap
            d += 1
            if d > self.cap:
                raise RuntimeError("full")
    def lookup(self, key):
        # PEDAGOGY-SOLUTION: D9-RH-LOOKUP
        idx = self._probe(key)
        d = 0
        while self.keys[idx] is not None and d <= self.cap:
            if self.keys[idx] == key:
                return idx
            if self.dist[idx] < d:
                return None
            idx = (idx + 1) % self.cap
            d += 1
        return None
