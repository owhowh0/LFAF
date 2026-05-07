from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
import re


class TokenType(Enum):
    LET = auto()
    PRINT = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    ASSIGN = auto()
    LPAREN = auto()
    RPAREN = auto()
    SEMICOLON = auto()
    COMMA = auto()
    EOF = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int


TOKEN_PATTERNS: list[tuple[TokenType | None, re.Pattern[str]]] = [
    (None, re.compile(r"[ \t\r]+")),
    (None, re.compile(r"\n")),
    (TokenType.STRING, re.compile(r'"([^"\\]|\\.)*"')),
    (TokenType.NUMBER, re.compile(r"\d+(?:\.\d+)?")),
    (TokenType.IDENTIFIER, re.compile(r"[A-Za-z_][A-Za-z0-9_]*")),
    (TokenType.PLUS, re.compile(r"\+")),
    (TokenType.MINUS, re.compile(r"-")),
    (TokenType.STAR, re.compile(r"\*")),
    (TokenType.SLASH, re.compile(r"/")),
    (TokenType.ASSIGN, re.compile(r"=")),
    (TokenType.LPAREN, re.compile(r"\(")),
    (TokenType.RPAREN, re.compile(r"\)")),
    (TokenType.SEMICOLON, re.compile(r";")),
    (TokenType.COMMA, re.compile(r",")),
]

KEYWORDS = {
    "let": TokenType.LET,
    "print": TokenType.PRINT,
}


class TokenizerError(ValueError):
    pass


def tokenize(source: str) -> list[Token]:
    tokens: list[Token] = []
    index = 0
    line = 1
    column = 1

    while index < len(source):
        matched = False

        for token_type, pattern in TOKEN_PATTERNS:
            match = pattern.match(source, index)
            if match is None:
                continue

            lexeme = match.group(0)
            matched = True

            if token_type is None:
                line_breaks = lexeme.count("\n")
                if line_breaks:
                    line += line_breaks
                    column = len(lexeme) - lexeme.rfind("\n")
                else:
                    column += len(lexeme)
                index = match.end()
                break

            if token_type is TokenType.IDENTIFIER and lexeme in KEYWORDS:
                token_type = KEYWORDS[lexeme]

            tokens.append(Token(token_type, lexeme, line, column))
            index = match.end()
            column += len(lexeme)
            break

        if matched:
            continue

        raise TokenizerError(f"Unexpected character {source[index]!r} at line {line}, column {column}")

    tokens.append(Token(TokenType.EOF, "", line, column))
    return tokens
