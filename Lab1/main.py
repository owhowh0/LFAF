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

for s, expected in tests:
    result = fa.string_belongs_to_language(s)
    print(f"String: {s}, Expected: {expected}, Result: {result}, {'PASS' if result == expected else 'FAIL'}")