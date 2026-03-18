from __future__ import annotations

import argparse
from pathlib import Path

from lexer import Lexer, LexerError


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Lexical scanner for a tiny scientific expression language"
    )
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        "--source",
        type=str,
        help="Inline source code to tokenize",
    )
    source_group.add_argument(
        "--file",
        type=Path,
        help="Path to a file containing source code",
    )
    return parser.parse_args()


def read_source(args: argparse.Namespace) -> str:
    if args.source is not None:
        return args.source
    return args.file.read_text(encoding="utf-8")


def main() -> None:
    args = parse_args()
    source = read_source(args)

    lexer = Lexer(source)
    try:
        tokens = lexer.tokenize()
    except LexerError as error:
        print(f"Lexical error: {error}")
        raise SystemExit(1)

    for token in tokens:
        print(token)


if __name__ == "__main__":
    main()
