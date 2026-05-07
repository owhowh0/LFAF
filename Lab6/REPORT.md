# Topic: Parsing and Building an Abstract Syntax Tree

### Course: Formal Languages & Finite Automata
### Author: Cretu Dumitru and cudos to the Vasile Drumea with Irina Cojuhari

----

## Theory

Parsing is the process of analyzing a stream of tokens and checking whether it follows a grammar. A parser does not only verify syntax; it also reveals the structural relationships between parts of the input. That structural view is useful because later stages of a compiler or interpreter can work with meaning instead of raw text.

An Abstract Syntax Tree (AST) is a hierarchical representation of the parsed input. Compared with a concrete parse tree, an AST removes punctuation and other syntactic noise, keeping only the nodes that matter for evaluation or semantic analysis. For example, in an arithmetic expression the operator becomes an internal node and the operands become children.

In this lab, the input language is a tiny statement-based expression language. It supports variable declarations, print statements, identifiers, numbers, strings, parentheses, and the four arithmetic operators. This is enough to demonstrate all the required ideas: token classification with regular expressions, recursive-descent parsing, and AST construction.

----

## Objectives

1. Use regular expressions to classify tokens with a `TokenType` enumeration.
2. Build data structures for an AST.
3. Implement a parser that extracts syntactic structure from the input text.
4. Provide a runnable example that shows both the token stream and the AST.

----

## Implementation Description

### 1. Tokenization with Regular Expressions

The lexical analysis is implemented in [tokenizer.py](tokenizer.py). Each token category is identified by a regular expression. Whitespace is skipped, identifiers are matched with a pattern for variable names, numbers are recognized as integers or decimals, and string literals are extracted with a quoted-string expression.

The tokenizer maps recognized lexemes to `TokenType` values. Keywords such as `let` and `print` are distinguished from ordinary identifiers after matching the identifier pattern. This keeps the logic simple while still satisfying the requirement to use regular expressions for token classification.

### 2. AST Data Structures

The AST nodes are defined in [ast_nodes.py](ast_nodes.py). The model uses small dataclasses for each syntactic construct: `Program`, `VarDeclaration`, `PrintStatement`, `ExpressionStatement`, `BinaryExpression`, `UnaryExpression`, `Literal`, and `Identifier`.

This structure follows the idea of abstraction layers. The `Program` node contains a list of statements, statements contain expressions, and expressions can recursively contain smaller expressions. That recursive shape is exactly what makes ASTs convenient for later interpretation or semantic checking.

### 3. Recursive-Descent Parser

The parser is implemented in [parser.py](parser.py). It uses a standard recursive-descent strategy with precedence levels:

* `expression` -> addition and subtraction
* `addition` -> multiplication/division terms combined with `+` and `-`
* `multiplication` -> unary factors combined with `*` and `/`
* `unary` -> negation
* `primary` -> literals, identifiers, and grouped expressions

Statements are parsed separately. The parser recognizes `let name = expression;` declarations, `print expression;` statements, and bare expression statements. Every statement must end with a semicolon, which makes the grammar explicit and easy to validate.

### 4. Demo Program

The entry point in [main.py](main.py) tokenizes a sample input, parses it, and prints both the token list and the AST as formatted JSON. This gives a direct way to inspect the syntactic structure and verify that the parser works correctly.

Example input used by the program:

```text
let total = 2 + 3 * (4 - 1);
let message = "sum ready";
print total;
print message;
```

----

## Conclusions / Results

This laboratory work demonstrates how parsing and AST construction can be implemented in Python without external parsing frameworks. The tokenizer uses regular expressions to classify input, the parser builds a hierarchical AST, and the final output makes the syntactic structure visible.

The resulting solution is small but complete: it recognizes a useful mini-language, preserves operator precedence, and produces a tree that can be extended later with evaluation or semantic analysis. The implementation is also easy to inspect, which is important for laboratory evaluation.

----

## References

1. Parsing Wiki: https://en.wikipedia.org/wiki/Parsing
2. Abstract Syntax Tree Wiki: https://en.wikipedia.org/wiki/Abstract_syntax_tree
3. Python `re` module documentation: https://docs.python.org/3/library/re.html
4. Your own implemented Python project in [Lab6](Lab6).