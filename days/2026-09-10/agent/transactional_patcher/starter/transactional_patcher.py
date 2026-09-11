class Patcher:
    def __init__(self, text):
        self.text = text
        self.snap = None
    def begin(self):
        # TODO [D8-PATCH-BEGIN]
        raise NotImplementedError("D8-PATCH-BEGIN")
    def apply(self, start, end, repl):
        # TODO [D8-PATCH-APPLY]
        raise NotImplementedError("D8-PATCH-APPLY")
    def commit(self):
        # TODO [D8-PATCH-COMMIT]
        raise NotImplementedError("D8-PATCH-COMMIT")
    def rollback(self):
        if self.snap is None:
            raise RuntimeError("no tx")
        self.text = self.snap
        self.snap = None
