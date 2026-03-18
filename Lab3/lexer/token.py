from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    # Single-character tokens
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    CARET = auto()
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    ASSIGN = auto()
    SEMICOLON = auto()

    # Literals and identifiers
    NUMBER = auto()
    IDENTIFIER = auto()

    # Keywords
    KW_LET = auto()
    KW_PRINT = auto()
    KW_SIN = auto()
    KW_COS = auto()
    KW_TAN = auto()

    EOF = auto()


@dataclass(frozen=True)
class Token:
    token_type: TokenType
    lexeme: str
    line: int
    column: int

    def __str__(self) -> str:
        return (
            f"{self.token_type.name:<12} "
            f"lexeme={self.lexeme!r:<14} "
            f"at {self.line}:{self.column}"
        )
