from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class ASTNode:
    pass


@dataclass(frozen=True)
class Program(ASTNode):
    statements: list[ASTNode]


@dataclass(frozen=True)
class VarDeclaration(ASTNode):
    name: str
    value: ASTNode


@dataclass(frozen=True)
class PrintStatement(ASTNode):
    value: ASTNode


@dataclass(frozen=True)
class ExpressionStatement(ASTNode):
    expression: ASTNode


@dataclass(frozen=True)
class BinaryExpression(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass(frozen=True)
class UnaryExpression(ASTNode):
    operator: str
    operand: ASTNode


@dataclass(frozen=True)
class Literal(ASTNode):
    value: Any


@dataclass(frozen=True)
class Identifier(ASTNode):
    name: str
