import unittest

from lexer import Lexer, LexerError, TokenType


class LexerTests(unittest.TestCase):
    def test_tokenizes_scientific_program(self) -> None:
        source = "let x = sin(0.5) + cos(0) - tan(1); print x;"
        token_types = [token.token_type for token in Lexer(source).tokenize()]

        expected = [
            TokenType.KW_LET,
            TokenType.IDENTIFIER,
            TokenType.ASSIGN,
            TokenType.KW_SIN,
            TokenType.LPAREN,
            TokenType.NUMBER,
            TokenType.RPAREN,
            TokenType.PLUS,
            TokenType.KW_COS,
            TokenType.LPAREN,
            TokenType.NUMBER,
            TokenType.RPAREN,
            TokenType.MINUS,
            TokenType.KW_TAN,
            TokenType.LPAREN,
            TokenType.NUMBER,
            TokenType.RPAREN,
            TokenType.SEMICOLON,
            TokenType.KW_PRINT,
            TokenType.IDENTIFIER,
            TokenType.SEMICOLON,
            TokenType.EOF,
        ]

        self.assertEqual(token_types, expected)

    def test_accepts_float_with_exponent(self) -> None:
        source = "let y = 6.022e23;"
        tokens = Lexer(source).tokenize()

        self.assertEqual(tokens[3].token_type, TokenType.NUMBER)
        self.assertEqual(tokens[3].lexeme, "6.022e23")

    def test_skips_comment(self) -> None:
        source = "let x = 1; # this should be ignored\nprint x;"
        token_types = [token.token_type for token in Lexer(source).tokenize()]

        self.assertIn(TokenType.KW_PRINT, token_types)
        self.assertEqual(token_types.count(TokenType.IDENTIFIER), 2)

    def test_invalid_exponent_raises(self) -> None:
        source = "let a = 10e+;"
        with self.assertRaises(LexerError):
            Lexer(source).tokenize()


if __name__ == "__main__":
    unittest.main()
