class HPStack:
    def __init__(self):
        self.head = None
        self.hazard = None
    def protect(self, node):
        # TODO [D9-HP-PROTECT]
        raise NotImplementedError
    def push(self, value):
        # TODO [D9-HP-PUSH]
        raise NotImplementedError
    def pop(self):
        # TODO [D9-HP-POP]
        raise NotImplementedError
