# PEDAGOGY-SOLUTION: TERM-ANSI-SGR-01
# PEDAGOGY-SOLUTION: TERM-CURSOR-02
"""Parser mínimo de sequências ANSI CSI."""


class AnsiParser:
    def __init__(self) -> None:
        self.fg = 7
        self.row = 0
        self.col = 0
        self.screen_text = ""

    def _apply_csi(self, params: str, final: str) -> None:
        values = (
            [int(x) if x else 0 for x in params.split(";")]
            if params
            else [0]
        )

        if final == "m":
            for value in values:
                if value == 0:
                    self.fg = 7
                elif value == 31:
                    self.fg = 1
        elif final == "H":
            row = values[0] if values and values[0] else 1
            col = values[1] if len(values) > 1 and values[1] else 1
            self.row = row - 1
            self.col = col - 1

    def feed(self, text: str) -> None:
        index = 0
        while index < len(text):
            if (
                text[index] == "\x1b"
                and index + 1 < len(text)
                and text[index + 1] == "["
            ):
                cursor = index + 2
                while cursor < len(text) and text[cursor] not in "mH":
                    cursor += 1
                if cursor >= len(text):
                    raise ValueError("incomplete CSI")
                self._apply_csi(text[index + 2 : cursor], text[cursor])
                index = cursor + 1
            else:
                self.screen_text += text[index]
                index += 1
