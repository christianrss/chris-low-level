class Patcher:
    def __init__(self, text):
        self.text = text
        self.snap = None
    def begin(self):
        # PEDAGOGY-SOLUTION: D8-PATCH-BEGIN
        self.snap = self.text
    def apply(self, start, end, repl):
        # PEDAGOGY-SOLUTION: D8-PATCH-APPLY
        if self.snap is None:
            raise RuntimeError("no tx")
        self.text = self.text[:start] + repl + self.text[end:]
    def commit(self):
        # PEDAGOGY-SOLUTION: D8-PATCH-COMMIT
        if self.snap is None:
            raise RuntimeError("no tx")
        self.snap = None
    def rollback(self):
        if self.snap is None:
            raise RuntimeError("no tx")
        self.text = self.snap
        self.snap = None
