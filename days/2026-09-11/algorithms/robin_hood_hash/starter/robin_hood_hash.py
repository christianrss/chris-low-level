class RobinHood:
    def __init__(self, cap=8):
        self.cap = cap
        self.keys = [None] * cap
        self.dist = [-1] * cap
    def _probe(self, key):
        # TODO [D9-RH-PROBE]
        raise NotImplementedError
    def insert(self, key):
        # TODO [D9-RH-INSERT]
        raise NotImplementedError
    def lookup(self, key):
        # TODO [D9-RH-LOOKUP]
        raise NotImplementedError
