from __future__ import annotations

from typing import Dict, List

from .token import Token, TokenType


class LexerError(ValueError):
    def __init__(self, message: str, line: int, column: int) -> None:
        super().__init__(f"{message} at line {line}, column {column}")


class Lexer:
    KEYWORDS: Dict[str, TokenType] = {
        "let": TokenType.KW_LET,
        "print": TokenType.KW_PRINT,
        "sin": TokenType.KW_SIN,
        "cos": TokenType.KW_COS,
        "tan": TokenType.KW_TAN,
    }

    SINGLE_CHAR_TOKENS: Dict[str, TokenType] = {
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "*": TokenType.STAR,
        "/": TokenType.SLASH,
        "^": TokenType.CARET,
        "(": TokenType.LPAREN,
        ")": TokenType.RPAREN,
        ",": TokenType.COMMA,
        "=": TokenType.ASSIGN,
        ";": TokenType.SEMICOLON,
    }

    def __init__(self, source: str) -> None:
        self.source = source
        self.current = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []

        while not self._is_at_end():
            self._skip_whitespace_and_comments()
            if self._is_at_end():
                break

            start_index = self.current
            start_line = self.line
            start_column = self.column
            current_char = self._peek()

            if current_char.isalpha() or current_char == "_":
                while self._peek().isalnum() or self._peek() == "_":
                    self._advance()

                lexeme = self.source[start_index:self.current]
                token_type = self.KEYWORDS.get(lexeme, TokenType.IDENTIFIER)
                tokens.append(Token(token_type, lexeme, start_line, start_column))
                continue

            if current_char.isdigit() or (
                current_char == "." and self._peek_next().isdigit()
            ):
                lexeme = self._scan_number(start_line, start_column)
                tokens.append(Token(TokenType.NUMBER, lexeme, start_line, start_column))
                continue

            token_type = self.SINGLE_CHAR_TOKENS.get(current_char)
            if token_type is not None:
                self._advance()
                tokens.append(Token(token_type, current_char, start_line, start_column))
                continue

            raise LexerError(
                f"Unexpected character {current_char!r}", start_line, start_column
            )

        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens

    def _scan_number(self, start_line: int, start_column: int) -> str:
        start_index = self.current
        has_dot = False

        if self._peek() == ".":
            has_dot = True
            self._advance()

        while self._peek().isdigit():
            self._advance()

        if self._peek() == "." and not has_dot:
            has_dot = True
            self._advance()
            while self._peek().isdigit():
                self._advance()

        if self._peek() in "eE":
            exponent_line = self.line
            exponent_column = self.column
            self._advance()

            if self._peek() in "+-":
                self._advance()

            if not self._peek().isdigit():
                raise LexerError(
                    "Malformed exponent in number literal",
                    exponent_line,
                    exponent_column,
                )

            while self._peek().isdigit():
                self._advance()

        return self.source[start_index:self.current]

    def _skip_whitespace_and_comments(self) -> None:
        while not self._is_at_end():
            current_char = self._peek()

            if current_char in " \r\t\n":
                self._advance()
                continue

            if current_char == "#":
                while not self._is_at_end() and self._peek() != "\n":
                    self._advance()
                continue

            break

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def _peek(self) -> str:
        if self._is_at_end():
            return "\0"
        return self.source[self.current]

    def _peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def _advance(self) -> str:
        char = self.source[self.current]
        self.current += 1

        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return char
