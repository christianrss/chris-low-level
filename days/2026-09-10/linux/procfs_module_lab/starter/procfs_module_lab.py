class ProcFS:
    def __init__(self):
        self.entries = {}
    def write(self, name, data):
        # TODO [D8-PROC-WRITE]
        raise NotImplementedError
    def read(self, name):
        # TODO [D8-PROC-READ]
        raise NotImplementedError
    def list(self):
        # TODO [D8-PROC-LIST]
        raise NotImplementedError
