class KVCacheRing:
    def __init__(self, capacity):
        if capacity <= 0: raise ValueError("capacity")
        self.capacity=capacity; self.keys=[None]*capacity; self.values=[None]*capacity
        self.positions=[None]*capacity; self.next_position=0
    def append(self, position, key, value):
        # TODO [D5-KV-APPEND]: grave K/V e tag lógico no slot circular.
        pass
    def window(self,start,end):
        # TODO [D5-KV-WINDOW]: valide tags e devolva janela.
        return []
    def reset(self):
        # TODO [D5-KV-RESET]: limpe ownership e cursor.
        pass
