PAGE = 4096

class TLB:
    def __init__(self):
        self.entries = {}
    def lookup(self, vaddr):
        # PEDAGOGY-SOLUTION: D8-TLB-LOOKUP
        vpn = vaddr // PAGE
        return self.entries.get(vpn)
    def walk(self, vaddr, page_table):
        # PEDAGOGY-SOLUTION: D8-TLB-WALK
        vpn = vaddr // PAGE
        if vpn not in page_table:
            raise KeyError("fault")
        return page_table[vpn]
    def fill(self, vpn, pfn):
        # PEDAGOGY-SOLUTION: D8-TLB-FILL
        self.entries[vpn] = pfn
