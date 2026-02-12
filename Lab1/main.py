import sys

from grammar import Grammar


g = Grammar()
fa = g.toFiniteAutomaton()

tests = [
        ("aca", True),
        ("acdbca", True),
        ("acddbca", True),
        ("ab", False),
        ("acd", False),
        ("bca", True)
    ]

all_passed = True

for s, expected in tests:
    result = fa.string_belongs_to_language(s)
    passed = result == expected
    if not passed:
        all_passed = False
    print(f"String: {s}, Expected: {expected}, Result: {result}, {'PASS' if passed else 'FAIL'}")

if not all_passed:
    sys.exit(1)