from __future__ import annotations

from .ast_nodes import (
    AssignStmt,
    BinaryOp,
    Call,
    Expr,
    ExprStmt,
    Function,
    IfStmt,
    LetStmt,
    Name,
    NumberLit,
    PrintStmt,
    Program,
    ReturnStmt,
    Stmt,
    UnaryOp,
    WhileStmt,
)
from .lexer import Kind, Token, tokenize


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.i = 0

    def _cur(self) -> Token:
        return self.tokens[self.i]

    def _advance(self) -> Token:
        tok = self.tokens[self.i]
        if tok.kind is not Kind.END:
            self.i += 1
        return tok

    def _expect(self, kind: Kind) -> Token:
        tok = self._cur()
        if tok.kind is not kind:
            raise SyntaxError(
                f"expected {kind.name}, got {tok.kind.name} ({tok.text!r}) at {tok.line}:{tok.col}"
            )
        return self._advance()

    def _match(self, *kinds: Kind) -> Token | None:
        if self._cur().kind in kinds:
            return self._advance()
        return None

    def parse(self) -> Program:
        functions: list[Function] = []
        main: list[Stmt] = []
        while self._cur().kind is not Kind.END:
            if self._cur().kind is Kind.FUNCTION:
                functions.append(self._function())
            else:
                main.append(self._stmt())
        return Program(functions=functions, main=main)

    def _function(self) -> Function:
        self._expect(Kind.FUNCTION)
        name = self._expect(Kind.IDENT).text
        self._expect(Kind.LPAREN)
        params: list[str] = []
        if self._cur().kind is not Kind.RPAREN:
            params.append(self._expect(Kind.IDENT).text)
            while self._match(Kind.COMMA):
                params.append(self._expect(Kind.IDENT).text)
        self._expect(Kind.RPAREN)
        body = self._block()
        return Function(name=name, params=params, body=body)

    def _block(self) -> list[Stmt]:
        self._expect(Kind.LBRACE)
        body: list[Stmt] = []
        while self._cur().kind is not Kind.RBRACE:
            if self._cur().kind is Kind.END:
                raise SyntaxError("unterminated block")
            body.append(self._stmt())
        self._expect(Kind.RBRACE)
        return body

    def _stmt(self) -> Stmt:
        k = self._cur().kind
        if k is Kind.LET or k is Kind.CONST:
            return self._let()
        if k is Kind.IF:
            return self._if()
        if k is Kind.WHILE:
            return self._while()
        if k is Kind.RETURN:
            self._advance()
            expr = self._expr()
            self._expect(Kind.SEMI)
            return ReturnStmt(expr)
        if k is Kind.PRINT:
            self._advance()
            self._expect(Kind.LPAREN)
            expr = self._expr()
            self._expect(Kind.RPAREN)
            self._expect(Kind.SEMI)
            return PrintStmt(expr)
        if k is Kind.IDENT and self.tokens[self.i + 1].kind is Kind.EQ:
            name = self._advance().text
            self._expect(Kind.EQ)
            expr = self._expr()
            self._expect(Kind.SEMI)
            return AssignStmt(name, expr)
        expr = self._expr()
        self._expect(Kind.SEMI)
        return ExprStmt(expr)

    def _let(self) -> LetStmt:
        is_const = self._cur().kind is Kind.CONST
        self._advance()
        name = self._expect(Kind.IDENT).text
        self._expect(Kind.EQ)
        expr = self._expr()
        self._expect(Kind.SEMI)
        return LetStmt(name=name, expr=expr, const=is_const)

    def _if(self) -> IfStmt:
        self._expect(Kind.IF)
        self._expect(Kind.LPAREN)
        cond = self._expr()
        self._expect(Kind.RPAREN)
        then_body = self._block()
        else_body: list[Stmt] = []
        if self._match(Kind.ELSE):
            else_body = self._block()
        return IfStmt(cond=cond, then_body=then_body, else_body=else_body)

    def _while(self) -> WhileStmt:
        self._expect(Kind.WHILE)
        self._expect(Kind.LPAREN)
        cond = self._expr()
        self._expect(Kind.RPAREN)
        body = self._block()
        return WhileStmt(cond=cond, body=body)

    def _expr(self) -> Expr:
        return self._cmp()

    def _cmp(self) -> Expr:
        left = self._add()
        while self._cur().kind in (Kind.EQEQ, Kind.NEQ, Kind.LT, Kind.LE, Kind.GT, Kind.GE):
            op_tok = self._advance()
            right = self._add()
            op_map = {
                Kind.EQEQ: "==",
                Kind.NEQ: "!=",
                Kind.LT: "<",
                Kind.LE: "<=",
                Kind.GT: ">",
                Kind.GE: ">=",
            }
            left = BinaryOp(op_map[op_tok.kind], left, right)
        return left

    def _add(self) -> Expr:
        left = self._mul()
        while self._cur().kind in (Kind.PLUS, Kind.MINUS):
            op = self._advance().text
            right = self._mul()
            left = BinaryOp(op, left, right)
        return left

    def _mul(self) -> Expr:
        left = self._unary()
        while self._cur().kind in (Kind.STAR, Kind.SLASH, Kind.PERCENT):
            op = self._advance().text
            right = self._unary()
            left = BinaryOp(op, left, right)
        return left

    def _unary(self) -> Expr:
        if self._cur().kind is Kind.MINUS:
            self._advance()
            return UnaryOp("-", self._unary())
        if self._cur().kind is Kind.BANG:
            self._advance()
            return UnaryOp("!", self._unary())
        return self._primary()

    def _primary(self) -> Expr:
        tok = self._cur()
        if tok.kind is Kind.NUMBER:
            self._advance()
            return NumberLit(tok.number)
        if tok.kind is Kind.IDENT:
            name = self._advance().text
            if self._match(Kind.LPAREN):
                args: list[Expr] = []
                if self._cur().kind is not Kind.RPAREN:
                    args.append(self._expr())
                    while self._match(Kind.COMMA):
                        args.append(self._expr())
                self._expect(Kind.RPAREN)
                return Call(name, args)
            return Name(name)
        if tok.kind is Kind.LPAREN:
            self._advance()
            expr = self._expr()
            self._expect(Kind.RPAREN)
            return expr
        raise SyntaxError(f"unexpected token {tok.kind.name} at {tok.line}:{tok.col}")


def parse_source(source: str) -> Program:
    return Parser(tokenize(source)).parse()
