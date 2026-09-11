import math
class SV:
    def __init__(self, nqubits):
        self.n = nqubits
        self.amp = [0.0] * (1 << nqubits)
        self.amp[0] = 1.0
    def set(self, mask, value):
        # PEDAGOGY-SOLUTION: D9-Q-SET
        self.amp[mask] = value
    def get(self, mask):
        # PEDAGOGY-SOLUTION: D9-Q-GET
        return self.amp[mask]
    def normalize(self):
        # PEDAGOGY-SOLUTION: D9-Q-NORM
        s = math.sqrt(sum(a*a for a in self.amp))
        if s == 0:
            return
        self.amp = [a / s for a in self.amp]
