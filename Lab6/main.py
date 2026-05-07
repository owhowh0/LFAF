from __future__ import annotations

from dataclasses import asdict, is_dataclass
import json

from ast_nodes import ASTNode
from parser import Parser
from tokenizer import tokenize


SAMPLE_SOURCE = """
let total = 2 + 3 * (4 - 1);
let message = "sum ready";
print total;
print message;
""".strip()


def ast_to_dict(node: ASTNode):
    if is_dataclass(node):
        data = asdict(node)
        data["type"] = node.__class__.__name__
        return data
    return node


def main() -> None:
    tokens = tokenize(SAMPLE_SOURCE)
    parser = Parser(tokens)
    program = parser.parse()

    print(
        json.dumps(
            [
                {
                    "type": token.type.name,
                    "lexeme": token.lexeme,
                    "line": token.line,
                    "column": token.column,
                }
                for token in tokens
            ],
            indent=2,
        )
    )
    print()
    print(json.dumps(ast_to_dict(program), indent=2))


if __name__ == "__main__":
    main()
