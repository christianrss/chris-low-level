from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class Kind(Enum):
    END = auto()
    NUMBER = auto()
    IDENT = auto()
    LET = auto()
    CONST = auto()
    FUNCTION = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    RETURN = auto()
    PRINT = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMI = auto()
    COMMA = auto()
    EQ = auto()  # assignment =
    EQEQ = auto()
    NEQ = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    BANG = auto()


KEYWORDS = {
    "let": Kind.LET,
    "const": Kind.CONST,
    "function": Kind.FUNCTION,
    "if": Kind.IF,
    "else": Kind.ELSE,
    "while": Kind.WHILE,
    "return": Kind.RETURN,
    "print": Kind.PRINT,
}


@dataclass
class Token:
    kind: Kind
    text: str = ""
    number: int = 0
    line: int = 1
    col: int = 1


class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1

    def _peek(self) -> str:
        return self.source[self.pos] if self.pos < len(self.source) else ""

    def _advance(self) -> str:
        ch = self.source[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def _skip(self) -> None:
        while True:
            while self._peek() and self._peek().isspace():
                self._advance()
            if self._peek() == "/" and self.pos + 1 < len(self.source) and self.source[self.pos + 1] == "/":
                while self._peek() and self._peek() != "\n":
                    self._advance()
                continue
            break

    def next(self) -> Token:
        self._skip()
        line, col = self.line, self.col
        if self.pos >= len(self.source):
            return Token(Kind.END, line=line, col=col)

        ch = self._peek()
        if ch.isdigit() or (ch == "-" and self.pos + 1 < len(self.source) and self.source[self.pos + 1].isdigit()):
            # numbers handled without leading '-'; unary handles negation
            pass
        if ch.isdigit():
            start = self.pos
            while self._peek().isdigit():
                self._advance()
            text = self.source[start : self.pos]
            return Token(Kind.NUMBER, text, int(text), line, col)

        if ch.isalpha() or ch == "_":
            start = self.pos
            self._advance()
            while self._peek().isalnum() or self._peek() == "_":
                self._advance()
            text = self.source[start : self.pos]
            kind = KEYWORDS.get(text, Kind.IDENT)
            return Token(kind, text, line=line, col=col)

        self._advance()
        nxt = self._peek()
        two = ch + nxt
        if two == "==":
            self._advance()
            return Token(Kind.EQEQ, two, line=line, col=col)
        if two == "!=":
            self._advance()
            return Token(Kind.NEQ, two, line=line, col=col)
        if two == "<=":
            self._advance()
            return Token(Kind.LE, two, line=line, col=col)
        if two == ">=":
            self._advance()
            return Token(Kind.GE, two, line=line, col=col)

        single = {
            "(": Kind.LPAREN,
            ")": Kind.RPAREN,
            "{": Kind.LBRACE,
            "}": Kind.RBRACE,
            ";": Kind.SEMI,
            ",": Kind.COMMA,
            "=": Kind.EQ,
            "<": Kind.LT,
            ">": Kind.GT,
            "+": Kind.PLUS,
            "-": Kind.MINUS,
            "*": Kind.STAR,
            "/": Kind.SLASH,
            "%": Kind.PERCENT,
            "!": Kind.BANG,
        }
        if ch in single:
            return Token(single[ch], ch, line=line, col=col)
        raise SyntaxError(f"unexpected character {ch!r} at {line}:{col}")


def tokenize(source: str) -> list[Token]:
    lex = Lexer(source)
    out: list[Token] = []
    while True:
        tok = lex.next()
        out.append(tok)
        if tok.kind is Kind.END:
            break
    return out
