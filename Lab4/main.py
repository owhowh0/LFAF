import random

# =============================================================================
#  AST Node Classes
# =============================================================================

class RegexNode:
    pass

class Literal(RegexNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self): return f"Literal('{self.value}')"

class Concatenation(RegexNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self): return f"Concat({self.left}, {self.right})"

class Alternation(RegexNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self): return f"Alt({self.left}, {self.right})"

class Repetition(RegexNode):
    def __init__(self, node, min_repeats, max_repeats):
        self.node = node
        self.min_repeats = min_repeats
        self.max_repeats = max_repeats
    def __repr__(self): return f"Rep({self.node}, {self.min_repeats}-{self.max_repeats})"


# =============================================================================
#  Tokenizer
#  Converts a regex string into a flat list of tokens.
#
#  Token types:
#    str         -> single-char operator: ( ) | * + ?
#    str         -> single-char literal: a-z, A-Z, 0-9, etc.
#    ('^', int)  -> exact repetition: ^N  (reads exactly ONE digit to avoid
#                   greedily consuming subsequent literal digits — BUG FIX)
#
#  Custom notation supported:
#    ^+   -> mapped to '+' (one-or-more, same as standard + operator)
#    ^N   -> exactly N repetitions (single digit)
# =============================================================================

def tokenize(regex_str):
    tokens = []
    i = 0
    while i < len(regex_str):
        c = regex_str[i]

        if c in '()|*+?':
            tokens.append(c)
            i += 1

        elif c == '^':
            if i + 1 < len(regex_str) and regex_str[i + 1] == '+':
                # ^+ means one-or-more, same as standard +
                tokens.append('+')
                i += 2
            elif i + 1 < len(regex_str) and regex_str[i + 1].isdigit():
                # BUG FIX: read exactly ONE digit so that e.g. (3|4)^5 36
                # does not consume the following '3' and '6' as part of the
                # repetition count (which would incorrectly give ^536 = 536).
                num = regex_str[i + 1]
                tokens.append(('^', int(num)))
                i += 2
            else:
                tokens.append(c)
                i += 1

        else:
            tokens.append(c)
            i += 1

    return tokens


# =============================================================================
#  Recursive Descent Parser
#  Builds an Abstract Syntax Tree (AST) from the token list.
#
#  Grammar (operator precedence low -> high):
#    expression    ::= alternation
#    alternation   ::= concatenation ( '|' concatenation )*
#    concatenation ::= repetition ( repetition )*
#    repetition    ::= primary ( '*' | '+' | '?' | ('^', N) )*
#    primary       ::= '(' expression ')' | LITERAL
# =============================================================================

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        return self.parse_alt()

    # --- alternation: lowest precedence ---------------------------------
    def parse_alt(self):
        node = self.parse_concat()
        while self.pos < len(self.tokens) and self.tokens[self.pos] == '|':
            self.pos += 1
            right = self.parse_concat()
            node = Alternation(node, right)
        return node

    # --- concatenation --------------------------------------------------
    def parse_concat(self):
        node = self.parse_rep()
        while self.pos < len(self.tokens) and self.tokens[self.pos] not in ('|', ')'):
            right = self.parse_rep()
            if right is None:
                break
            node = Concatenation(node, right)
        return node

    # --- repetition: highest precedence ---------------------------------
    def parse_rep(self):
        node = self.parse_primary()
        if node is None:
            return None

        while self.pos < len(self.tokens):
            t = self.tokens[self.pos]
            if t == '*':
                node = Repetition(node, 0, 5)   # cap at 5 (task requirement)
                self.pos += 1
            elif t == '+':
                node = Repetition(node, 1, 5)   # cap at 5
                self.pos += 1
            elif t == '?':
                node = Repetition(node, 0, 1)
                self.pos += 1
            elif isinstance(t, tuple) and t[0] == '^':
                node = Repetition(node, t[1], t[1])   # exact repetition
                self.pos += 1
            else:
                break
        return node

    # --- primary --------------------------------------------------------
    def parse_primary(self):
        if self.pos >= len(self.tokens):
            return None
        t = self.tokens[self.pos]
        if t == '(':
            self.pos += 1
            node = self.parse_alt()
            if self.pos < len(self.tokens) and self.tokens[self.pos] == ')':
                self.pos += 1
            return node
        elif isinstance(t, tuple):
            # A bare repetition tuple without a preceding primary is invalid;
            # return None so the caller can stop.
            return None
        else:
            self.pos += 1
            return Literal(t)


# =============================================================================
#  Generator
#  Walks the AST recursively and produces a random valid string.
#
#  Debug mode prints a numbered step log showing which operation is
#  performed at each stage of the traversal (bonus task).
# =============================================================================

class Generator:
    def __init__(self, debug=False):
        self.debug = debug

    def generate_random(self, node, step_counter=None):
        # FIX: don't rely on mutable default argument — always create a fresh
        # counter when one is not explicitly provided by the caller.
        if step_counter is None:
            step_counter = [1]

        if isinstance(node, Literal):
            if self.debug:
                print(f"  [{step_counter[0]:>3}] Literal          -> '{node.value}'")
            step_counter[0] += 1
            return node.value

        elif isinstance(node, Concatenation):
            if self.debug:
                print(f"  [{step_counter[0]:>3}] Concatenation    (evaluating left then right)")
            step_counter[0] += 1
            left  = self.generate_random(node.left,  step_counter)
            right = self.generate_random(node.right, step_counter)
            return left + right

        elif isinstance(node, Alternation):
            if self.debug:
                print(f"  [{step_counter[0]:>3}] Alternation      (choosing one branch)")
            step_counter[0] += 1
            if random.random() < 0.5:
                if self.debug: print("         >> Selected LEFT branch")
                return self.generate_random(node.left, step_counter)
            else:
                if self.debug: print("         >> Selected RIGHT branch")
                return self.generate_random(node.right, step_counter)

        elif isinstance(node, Repetition):
            repeats = random.randint(node.min_repeats, node.max_repeats)
            if self.debug:
                print(f"  [{step_counter[0]:>3}] Repetition       [{node.min_repeats}..{node.max_repeats}]"
                      f" -> repeating {repeats} time(s)")
            step_counter[0] += 1
            result = ""
            for rep_i in range(repeats):
                if self.debug:
                    print(f"         -- iteration {rep_i + 1}/{repeats}")
                result += self.generate_random(node.node, step_counter)
            return result

        return ""


# =============================================================================
#  process_regex  —  high-level helper
#  Tokenizes, parses, and generates `generate_count` sample strings for one
#  regex.  The first generated string is printed with full debug trace;
#  subsequent ones are generated silently and collected in a set.
# =============================================================================

def process_regex(regex, debug=False, generate_count=5):
    print(f"\n{'='*60}")
    print(f"  Regular Expression : {regex}")
    print(f"{'='*60}")

    tokens = tokenize(regex)
    print(f"  Tokens             : {tokens}")

    parser = Parser(tokens)
    ast    = parser.parse()
    print(f"  AST                : {ast}")
    print()

    generator = Generator(debug=False)
    results   = []

    for i in range(generate_count):
        # Show full step-by-step trace only for the first string
        first = (i == 0 and debug)
        if first:
            print("  --- Step-by-step trace for string #1 ---")
            generator.debug = True
            word = generator.generate_random(ast)
            generator.debug = False
            print(f"  => Generated: '{word}'")
            print()
        else:
            word = generator.generate_random(ast)

        results.append(word)

    print("  Generated strings:")
    for idx, w in enumerate(results, 1):
        print(f"    [{idx}] '{w}'")
    print()


# =============================================================================
#  Entry point
# =============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("  VARIANT 1 — Regex String Generator")
    print("=" * 60)

    # NOTE on Regex 3 input:
    #   The original task expression is  1(0|1)*2(3|4)^5 36
    #   meaning: (3|4) repeated exactly 5 times, then literals '3' and '6'.
    #   We write it as "1(0|1)*2(3|4)^536" but the FIXED tokenizer now reads
    #   only ONE digit after '^', so '^5' is parsed as repeat-5 and '3','6'
    #   become separate literal tokens — exactly as intended.
    regexes_v1 = [
        "(a|b)(c|d)E^+G?",
        "P(Q|R|S)T(UV|W|X)*Z^+",
        "1(0|1)*2(3|4)^536",
    ]

    for regex in regexes_v1:
        process_regex(regex, debug=True, generate_count=5)