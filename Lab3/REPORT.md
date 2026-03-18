# Scientific Expression Lexer in Python

### Course: Formal Languages & Finite Automata
### Author: Name Surname (Preferably yours!)

----

## Theory

Lexical analysis is the process of transforming a raw stream of characters into meaningful token units. A lexer does not execute expressions and does not validate deep syntax rules; instead, it classifies lexemes into categories such as identifiers, literals, keywords, operators, and separators. This stage is important because it prepares a clean token stream for the next compiler or interpreter phase (typically parsing).

In this laboratory work, the lexer is implemented for a small scientific expression language, not only for basic arithmetic. The scanner supports integer and floating-point literals, scientific notation, variables, assignment, printing statements, and trigonometric keywords (`sin`, `cos`, `tan`).

## Objectives

- Understand how lexical analysis transforms source code into tokens.
- Implement a lexer in Python with clear token categories.
- Support a richer input than a simple calculator by including trigonometric operations and float/exponent numbers.
- Demonstrate lexer behavior with a sample input and tests.

## Implementation description

The implementation is split into focused modules. `lexer/token.py` defines token categories (`TokenType`) and a `Token` data object that stores token type, lexeme, and source position (line/column).

`lexer/lexer.py` contains the scanner logic. It traverses the source character by character, skips whitespace and comments, and emits tokens for identifiers, keywords, numbers, and punctuation. It also reports lexical errors when it finds unsupported characters or malformed number exponents.

`main.py` is a small CLI front-end. It accepts input either from a file (`--file`) or directly as a string (`--source`), runs the lexer, and prints one token per line.

### Core token model (`lexer/token.py`)

```python
class TokenType(Enum):
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
    NUMBER = auto()
    IDENTIFIER = auto()
    KW_LET = auto()
    KW_PRINT = auto()
    KW_SIN = auto()
    KW_COS = auto()
    KW_TAN = auto()
    EOF = auto()
```

### Lexer keyword and operator maps (`lexer/lexer.py`)

```python
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
```

### Number scanning with float and exponent support (`lexer/lexer.py`)

```python
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
```

### CLI usage (`main.py`)

```python
python3 main.py --file examples/program.lx
python3 main.py --source "let x = sin(0.5) + cos(0); print x;"
```

## Conclusions / Screenshots / Results

The implemented lexer satisfies the laboratory objective: it transforms source code into a stream of typed tokens with position metadata. Compared with a minimal calculator scanner, this solution is more expressive because it supports variables, statements, trigonometric keywords, and both integer and floating-point scientific literals. The project also includes tests that verify expected tokenization behavior and error handling.

## References

1. LLVM Tutorial, *A sample of a lexer implementation*: https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html
2. Wikipedia, *Lexical analysis*: https://en.wikipedia.org/wiki/Lexical_analysis
