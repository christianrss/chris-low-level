import math
class SV:
    def __init__(self, nqubits):
        self.n = nqubits
        self.amp = [0.0] * (1 << nqubits)
        self.amp[0] = 1.0
    def set(self, mask, value):
        # TODO [D9-Q-SET]
        raise NotImplementedError
    def get(self, mask):
        # TODO [D9-Q-GET]
        raise NotImplementedError
    def normalize(self):
        # TODO [D9-Q-NORM]
        raise NotImplementedError
