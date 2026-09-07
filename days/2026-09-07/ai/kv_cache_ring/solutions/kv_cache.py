class KVCacheRing:
    def __init__(self, capacity):
        if capacity <= 0: raise ValueError("capacity")
        self.capacity=capacity; self.keys=[None]*capacity; self.values=[None]*capacity
        self.positions=[None]*capacity; self.next_position=0
    def append(self, position, key, value):
        # PEDAGOGY-SOLUTION: D5-KV-APPEND
        if position != self.next_position: raise ValueError("non-contiguous position")
        slot=position%self.capacity; self.keys[slot]=key; self.values[slot]=value
        self.positions[slot]=position; self.next_position+=1
    def window(self,start,end):
        # PEDAGOGY-SOLUTION: D5-KV-WINDOW
        if start<0 or end<start or end>self.next_position: raise ValueError("invalid window")
        out=[]
        for p in range(start,end):
            slot=p%self.capacity
            if self.positions[slot]!=p: raise KeyError(f"position {p} was evicted")
            out.append((self.keys[slot],self.values[slot]))
        return out
    def reset(self):
        # PEDAGOGY-SOLUTION: D5-KV-RESET
        self.positions=[None]*self.capacity; self.keys=[None]*self.capacity
        self.values=[None]*self.capacity; self.next_position=0
