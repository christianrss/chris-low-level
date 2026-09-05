"""Parser mínimo de sequências ANSI CSI para terminal educacional."""


class AnsiParser:
    """Mantém estado de cursor, cor e texto visível."""

    def __init__(self) -> None:
        self.fg = 7
        self.row = 0
        self.col = 0
        self.screen_text = ""

    def _apply_csi(self, params: str, final: str) -> None:
        """Aplica um comando CSI já tokenizado.

        TODO [TERM-ANSI-SGR-01]: interpretar SGR (reset e vermelho).
        TODO [TERM-CURSOR-02]: interpretar cursor H (linha;coluna 1-based).
        """
        raise NotImplementedError

    def feed(self, text: str) -> None:
        """Processa texto misto (literal + escape sequences).

        TODO [TERM-ANSI-SGR-01] [TERM-CURSOR-02]: separar texto normal de CSI.
        """
        raise NotImplementedError
