class Terminal:
    def __init__(self): self.fg=7; self.row=0; self.col=0; self.screen_text=''
    def feed(self,text):
        # TODO [TERM-ANSI-SGR-01] + [TERM-CURSOR-02]
        self.screen_text += text
