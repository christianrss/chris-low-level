class TwoBit:
    def __init__(self):
        # PEDAGOGY-SOLUTION: D7-BR-INIT
        self.state = 1  # 0,1 not-taken; 2,3 taken
    def predict(self):
        # PEDAGOGY-SOLUTION: D7-BR-PRED
        return self.state >= 2
    def update(self, taken: bool):
        # PEDAGOGY-SOLUTION: D7-BR-UPDATE
        if taken:
            self.state = min(3, self.state + 1)
        else:
            self.state = max(0, self.state - 1)
