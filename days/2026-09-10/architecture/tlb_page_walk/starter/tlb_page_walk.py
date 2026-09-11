PAGE = 4096

class TLB:
    def __init__(self):
        self.entries = {}
    def lookup(self, vaddr):
        # TODO [D8-TLB-LOOKUP]
        raise NotImplementedError("D8-TLB-LOOKUP")
    def walk(self, vaddr, page_table):
        # TODO [D8-TLB-WALK]
        raise NotImplementedError("D8-TLB-WALK")
    def fill(self, vpn, pfn):
        # TODO [D8-TLB-FILL]
        raise NotImplementedError("D8-TLB-FILL")
