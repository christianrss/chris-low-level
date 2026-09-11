class TaggedFreelist:
    def __init__(self, n):
        self.nodes = [{"next": i+1, "tag": 0} for i in range(n)]
        self.nodes[-1]["next"] = None
        self.head = 0
        self.head_tag = 0
    def pack(self, idx, tag):
        # PEDAGOGY-SOLUTION: D8-ABA-TAG
        return (idx & 0xFFFF) | ((tag & 0xFFFF) << 16)
    def push(self, idx):
        # PEDAGOGY-SOLUTION: D8-ABA-PUSH
        self.nodes[idx]["next"] = self.head
        self.nodes[idx]["tag"] = self.head_tag
        self.head = idx
        self.head_tag = (self.head_tag + 1) & 0xFFFF
    def pop(self):
        # PEDAGOGY-SOLUTION: D8-ABA-POP
        if self.head is None:
            return None
        idx = self.head
        nxt = self.nodes[idx]["next"]
        self.head = nxt
        self.head_tag = (self.head_tag + 1) & 0xFFFF
        return idx
