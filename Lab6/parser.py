from __future__ import annotations

from dataclasses import dataclass

from ast_nodes import (
    BinaryExpression,
    ExpressionStatement,
    Identifier,
    Literal,
    PrintStatement,
    Program,
    UnaryExpression,
    VarDeclaration,
)
from tokenizer import Token, TokenType


class ParserError(ValueError):
    pass


@dataclass
class Parser:
    tokens: list[Token]
    current: int = 0

    def parse(self) -> Program:
        statements = []
        while not self._is_at_end():
            statements.append(self._statement())
        return Program(statements)

    def _statement(self):
        if self._match(TokenType.LET):
            return self._var_declaration()
        if self._match(TokenType.PRINT):
            value = self._expression()
            self._consume(TokenType.SEMICOLON, "Expected ';' after print statement.")
            return PrintStatement(value)

        expression = self._expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after expression.")
        return ExpressionStatement(expression)

    def _var_declaration(self) -> VarDeclaration:
        name = self._consume(TokenType.IDENTIFIER, "Expected variable name after 'let'.")
        self._consume(TokenType.ASSIGN, "Expected '=' after variable name.")
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after variable declaration.")
        return VarDeclaration(name.lexeme, value)

    def _expression(self):
        return self._addition()

    def _addition(self):
        node = self._multiplication()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous().lexeme
            right = self._multiplication()
            node = BinaryExpression(node, operator, right)
        return node

    def _multiplication(self):
        node = self._unary()
        while self._match(TokenType.STAR, TokenType.SLASH):
            operator = self._previous().lexeme
            right = self._unary()
            node = BinaryExpression(node, operator, right)
        return node

    def _unary(self):
        if self._match(TokenType.MINUS):
            operator = self._previous().lexeme
            return UnaryExpression(operator, self._unary())
        return self._primary()

    def _primary(self):
        if self._match(TokenType.NUMBER):
            lexeme = self._previous().lexeme
            value = float(lexeme) if "." in lexeme else int(lexeme)
            return Literal(value)

        if self._match(TokenType.STRING):
            lexeme = self._previous().lexeme
            return Literal(lexeme[1:-1])

        if self._match(TokenType.IDENTIFIER):
            return Identifier(self._previous().lexeme)

        if self._match(TokenType.LPAREN):
            expression = self._expression()
            self._consume(TokenType.RPAREN, "Expected ')' after expression.")
            return expression

        token = self._peek()
        raise ParserError(f"Unexpected token {token.lexeme!r} at line {token.line}, column {token.column}")

    def _match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if self._check(token_type):
            return self._advance()
        token = self._peek()
        raise ParserError(f"{message} Got {token.lexeme!r} at line {token.line}, column {token.column}.")

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().type == token_type

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]
