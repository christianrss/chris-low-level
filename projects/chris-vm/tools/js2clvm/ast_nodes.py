from __future__ import annotations

from dataclasses import dataclass, field
from typing import Union


@dataclass
class NumberLit:
    value: int


@dataclass
class Name:
    ident: str


@dataclass
class UnaryOp:
    op: str  # '-' | '!'
    expr: "Expr"


@dataclass
class BinaryOp:
    op: str
    left: "Expr"
    right: "Expr"


@dataclass
class Call:
    callee: str
    args: list["Expr"]


@dataclass
class BuiltinPrint:
    arg: "Expr"


Expr = Union[NumberLit, Name, UnaryOp, BinaryOp, Call, BuiltinPrint]


@dataclass
class LetStmt:
    name: str
    expr: Expr
    const: bool = False


@dataclass
class AssignStmt:
    name: str
    expr: Expr


@dataclass
class IfStmt:
    cond: Expr
    then_body: list["Stmt"]
    else_body: list["Stmt"] = field(default_factory=list)


@dataclass
class WhileStmt:
    cond: Expr
    body: list["Stmt"]


@dataclass
class ReturnStmt:
    expr: Expr


@dataclass
class ExprStmt:
    expr: Expr


@dataclass
class PrintStmt:
    expr: Expr


Stmt = Union[LetStmt, AssignStmt, IfStmt, WhileStmt, ReturnStmt, ExprStmt, PrintStmt]


@dataclass
class Function:
    name: str
    params: list[str]
    body: list[Stmt]


@dataclass
class Program:
    functions: list[Function]
    main: list[Stmt]
