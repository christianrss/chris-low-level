class ProcFS:
    def __init__(self):
        self.entries = {}
    def write(self, name, data):
        # PEDAGOGY-SOLUTION: D8-PROC-WRITE
        self.entries[name] = str(data)
    def read(self, name):
        # PEDAGOGY-SOLUTION: D8-PROC-READ
        if name not in self.entries:
            raise KeyError(name)
        return self.entries[name]
    def list(self):
        # PEDAGOGY-SOLUTION: D8-PROC-LIST
        return sorted(self.entries)
