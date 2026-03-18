# Lexer and Scanner Lab (Python)

This project implements a lexer (scanner/tokenizer) for a tiny scientific expression language.
The lexer recognizes:
- Keywords: `let`, `print`, `sin`, `cos`, `tan`
- Numbers: integers, floating-point values, and exponent notation (for example `2`, `3.14`, `.5`, `6.022e23`)
- Identifiers: variable names such as `radius`, `value1`
- Operators and punctuation: `+ - * / ^ ( ) , = ;`
- Comments: lines starting with `#`

## Run

```bash
python3 main.py --file examples/program.lx
```

Or with inline source:

```bash
python3 main.py --source "let x = sin(0.5) + cos(0); print x;"
```

## Run tests

```bash
python3 -m unittest discover -s tests -v
```
