class TaggedFreelist:
    def __init__(self, n):
        self.nodes = [{"next": i+1, "tag": 0} for i in range(n)]
        self.nodes[-1]["next"] = None
        self.head = 0  # index
        self.head_tag = 0
    def push(self, idx):
        # TODO [D8-ABA-PUSH]
        raise NotImplementedError("D8-ABA-PUSH")
    def pop(self):
        # TODO [D8-ABA-POP]
        raise NotImplementedError("D8-ABA-POP")
    def pack(self, idx, tag):
        # TODO [D8-ABA-TAG]
        raise NotImplementedError("D8-ABA-TAG")
