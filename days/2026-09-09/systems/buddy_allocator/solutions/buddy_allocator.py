class Buddy:
    def __init__(self, size):
        # PEDAGOGY-SOLUTION: D7-BUDDY-INIT
        if size < 1 or (size & (size - 1)) != 0:
            raise ValueError("size power of two")
        self.size = size
        self.free = {size: [0]}
        self.used = {}
    def alloc(self, n):
        # PEDAGOGY-SOLUTION: D7-BUDDY-ALLOC
        need = 1
        while need < n:
            need <<= 1
        if need > self.size:
            return None
        order = need
        while order <= self.size and not self.free.get(order):
            order <<= 1
        if order > self.size or not self.free.get(order):
            return None
        idx = self.free[order].pop(0)
        while order > need:
            order >>= 1
            self.free.setdefault(order, []).append(idx + order)
            self.free[order].sort()
        self.used[idx] = need
        return idx
    def free(self, idx):
        # PEDAGOGY-SOLUTION: D7-BUDDY-FREE
        if idx not in self.used:
            raise KeyError(idx)
        order = self.used.pop(idx)
        while order < self.size:
            buddy = idx ^ order
            lst = self.free.setdefault(order, [])
            if buddy in lst:
                lst.remove(buddy)
                idx = min(idx, buddy)
                order <<= 1
                continue
            lst.append(idx)
            lst.sort()
            return
        self.free.setdefault(self.size, []).append(0)
