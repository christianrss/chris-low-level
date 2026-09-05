class Terminal:
    def __init__(self):
        self.fg = 7
        self.row = 0
        self.col = 0
        self.screen_text = ''

    def _apply_csi(self, params, final):
        if final == 'm':
            # TODO [TERM-ANSI-SGR-01]: reset e cor vermelha
            raise NotImplementedError
        if final == 'H':
            # TODO [TERM-CURSOR-02]: row;col 1-based -> 0-based
            raise NotImplementedError

    def feed(self, text):
        # TODO [TERM-ANSI-SGR-01] [TERM-CURSOR-02]: separar texto normal de CSI
        raise NotImplementedError
