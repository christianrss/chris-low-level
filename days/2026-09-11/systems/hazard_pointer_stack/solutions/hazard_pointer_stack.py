class HPStack:
    def __init__(self):
        self.head = None
        self.hazard = None
    def protect(self, node):
        # PEDAGOGY-SOLUTION: D9-HP-PROTECT
        self.hazard = node
        return node
    def push(self, value):
        # PEDAGOGY-SOLUTION: D9-HP-PUSH
        node = {"value": value, "next": self.head}
        self.head = node
    def pop(self):
        # PEDAGOGY-SOLUTION: D9-HP-POP
        node = self.protect(self.head)
        if node is None:
            return None
        self.head = node["next"]
        if self.hazard is node:
            self.hazard = None
        return node["value"]
