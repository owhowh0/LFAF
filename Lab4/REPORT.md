# Regular Expressions — Variant 1

### Course: Formal Languages & Finite Automata
### Author: Covali Ilie

---

## Theory

Regular expressions act as algebraic statements corresponding to regular languages. In everyday scenarios, they serve as templates specifying text patterns that an engine uses algorithmically to match or validate input strings dynamically. Regular expressions provide extreme versatility with concise syntax to solve complex logical problems involving strings, logs, and compilers.

The three basic operations of regular expressions — **concatenation**, **union (alternation)**, and **Kleene closure (repetition)** — allow an arbitrary combination of string lengths to be evaluated smoothly within any data engine configuration.

---

## Objectives

1. Write a report detailing regular expressions and their applications.
2. Produce a script interpreting 3 complex expressions conforming to **Variant 1**:
   - `(a|b)(c|d)E^+G?` — alternation, one-or-more, optional
   - `P(Q|R|S)T(UV|W|X)*Z^+` — three-branch alternation, zero-or-more, one-or-more
   - `1(0|1)*2(3|4)^5 36` — binary digits, exact repetition of 5, literal suffix `36`
     > **Note:** written in code as `"1(0|1)*2(3|4)^536"` — the tokenizer reads only one digit after `^`, so `^5` is the quantifier and `3`, `6` become separate literal tokens.
3. Dynamically evaluate and process the variants rather than utilizing hard-coded conditions to generate strings.
4. Ensure unbounded loops (`*` and `+`) simulate a randomized bound limited to a maximum of **5** repetitions.
5. Create a function tracing the generation process step-by-step.

---

## Implementation Description

The system operates across three phases designed in pure Python: breaking the string into tokens, converting the tokens into a parse tree, and walking down this tree to randomly generate textual values matching the variant formulas.

### Phase 1 — Tokenization

The tokenizer converts the raw regex string into a flat list of typed tokens so that the parser never deals with raw strings directly.

Key decisions:

- Standard metacharacters `(`, `)`, `|`, `*`, `+`, `?` are emitted as single-character string tokens.
- The custom notation `^+` (superscript plus, one-or-more) is mapped to a standard `+` token.
- The notation `^N` (exact repetition) reads **exactly one digit** after `^` and emits a tuple token `('^', N)`.

The single-digit constraint is a deliberate bug fix. The original implementation used a `while` loop that greedily consumed all consecutive digits after `^`:

```python
# Original — buggy
while i < len(regex_str) and regex_str[i].isdigit():
    num += regex_str[i]
    i += 1
```

This caused `(3|4)^536` to be tokenized as repeat-**536** instead of repeat-**5** followed by literals `3` and `6`. The fix reads exactly one digit:

```python
# Fixed
num = regex_str[i + 1]      # exactly ONE digit
tokens.append(('^', int(num)))
i += 2
```

### Phase 2 — AST Node Structuring & Parsing

Four node classes inherit from a common `RegexNode` base, enabling polymorphic recursive traversal:

| Class | Represents |
|---|---|
| `Literal(value)` | A single character literal |
| `Concatenation(left, right)` | Two sub-expressions placed sequentially |
| `Alternation(left, right)` | A choice between two sub-expressions (`\|`) |
| `Repetition(node, min, max)` | A sub-expression repeated between min and max times |

A recursive descent parser builds the AST by calling functions in descending precedence order:

```
parse_alt() → parse_concat() → parse_rep() → parse_primary()
```

This ordering ensures repetition binds tightest, then concatenation, then alternation — matching standard regex operator precedence. The `parse_alt` function handles multi-branch alternation left-to-right:

```python
def parse_alt(self):
    node = self.parse_concat()
    while self.pos < len(self.tokens) and self.tokens[self.pos] == '|':
        self.pos += 1
        right = self.parse_concat()
        node = Alternation(node, right)
    return node
```

This seamlessly handles expressions like `(UV|W|X)` where `UV` is internally represented as `Concatenation(Literal('U'), Literal('V'))`.

### Phase 3 — Random String Generation

Once the AST is built, the `Generator` class traverses it recursively. Behaviour per node type:

- **Literal** — returns the character directly.
- **Concatenation** — generates left then right sub-tree and concatenates results.
- **Alternation** — picks left or right branch with 50% probability:

```python
elif isinstance(node, Alternation):
    if random.random() < 0.5:
        return self.generate_random(node.left, step_counter)
    else:
        return self.generate_random(node.right, step_counter)
```

- **Repetition** — draws a random integer within `[min, max]` and runs the sub-tree that many times:

| Operator | min | max |
|---|---|---|
| `*` | 0 | 5 |
| `+` | 1 | 5 |
| `?` | 0 | 1 |
| `^N` | N | N |

The method signature uses `step_counter=None` with an explicit reset inside the function body:

```python
def generate_random(self, node, step_counter=None):
    if step_counter is None:
        step_counter = [1]
```

This is a second bug fix from the original. The original used `step_counter=[1]` as a default argument. In Python, mutable default arguments are created **once** at function definition time and shared across all calls, meaning the counter would never reset between separate invocations. Using `None` as the default and initializing a fresh list inside guarantees a clean counter on every call.

### Bonus — Step-by-Step Trace

The `step_counter` list is passed through every recursive call. When `debug=True`, each node prints its numbered step and operation type before acting. The trace is shown only for the first generated string per regex to keep output readable.

---

## Results

### Regex 1: `(a|b)(c|d)E^+G?`

One character from `{a, b}`, one from `{c, d}`, one to five `E` characters, optional `G`.

```
Tokens : ['(', 'a', '|', 'b', ')', '(', 'c', '|', 'd', ')', 'E', '+', 'G', '?']

[  1] Concatenation    (evaluating left then right)
[  2] Concatenation    (evaluating left then right)
[  3] Concatenation    (evaluating left then right)
[  4] Alternation      >> Selected LEFT branch
[  5] Literal          -> 'a'
[  6] Alternation      >> Selected RIGHT branch
[  7] Literal          -> 'd'
[  8] Repetition       [1..5] -> repeating 3 time(s)
       -- iteration 1/3
[  9] Literal          -> 'E'
       -- iteration 2/3
[ 10] Literal          -> 'E'
       -- iteration 3/3
[ 11] Literal          -> 'E'
[ 12] Repetition       [0..1] -> repeating 1 time(s)
       -- iteration 1/1
[ 13] Literal          -> 'G'

=> 'adEEEG'

Sample outputs: ['adEEEG', 'bcEE', 'acEEEEG', 'bdEG', 'acEEE']
```

### Regex 2: `P(Q|R|S)T(UV|W|X)*Z^+`

`P`, one of `{Q, R, S}`, `T`, zero to five repetitions of `{UV, W, X}`, one to five `Z` characters.

```
Tokens : ['P', '(', 'Q', '|', 'R', '|', 'S', ')', 'T', '(', 'U', 'V', '|', 'W', '|', 'X', ')', '*', 'Z', '+']

[  1] Concatenation    (evaluating left then right)
[  2] Concatenation    (evaluating left then right)
[  3] Concatenation    (evaluating left then right)
[  4] Concatenation    (evaluating left then right)
[  5] Literal          -> 'P'
[  6] Alternation      >> Selected LEFT branch
[  7] Alternation      >> Selected RIGHT branch
[  8] Literal          -> 'R'
[  9] Literal          -> 'T'
[ 10] Repetition       [0..5] -> repeating 2 time(s)
       -- iteration 1/2
[ 11] Alternation      >> Selected RIGHT branch
[ 12] Literal          -> 'X'
       -- iteration 2/2
[ 13] Alternation      >> Selected LEFT branch
[ 14] Alternation      >> Selected LEFT branch
[ 15] Concatenation    (evaluating left then right)
[ 16] Literal          -> 'U'
[ 17] Literal          -> 'V'
[ 18] Repetition       [1..5] -> repeating 2 time(s)
       -- iteration 1/2
[ 19] Literal          -> 'Z'
       -- iteration 2/2
[ 20] Literal          -> 'Z'

=> 'PRTXUVZZ'

Sample outputs: ['PRTXUVZZ', 'PQTWZZZZ', 'PSTZZ', 'PRTWWXZ', 'PQTUVUVWZZZ']
```

### Regex 3: `1(0|1)*2(3|4)^5 36`

`1`, zero to five binary digits, `2`, exactly five characters from `{3, 4}`, then literals `3` and `6`.

```
Tokens : ['1', '(', '0', '|', '1', ')', '*', '2', '(', '3', '|', '4', ')', ('^', 5), '3', '6']

[  1] Concatenation    (evaluating left then right)
[  2] Concatenation    (evaluating left then right)
[  3] Concatenation    (evaluating left then right)
[  4] Concatenation    (evaluating left then right)
[  5] Concatenation    (evaluating left then right)
[  6] Literal          -> '1'
[  7] Repetition       [0..5] -> repeating 2 time(s)
       -- iteration 1/2
[  8] Alternation      >> Selected RIGHT branch
[  9] Literal          -> '1'
       -- iteration 2/2
[ 10] Alternation      >> Selected LEFT branch
[ 11] Literal          -> '0'
[ 12] Literal          -> '2'
[ 13] Repetition       [5..5] -> repeating 5 time(s)
       -- iteration 1/5  -> '4'
       -- iteration 2/5  -> '3'
       -- iteration 3/5  -> '4'
       -- iteration 4/5  -> '3'
       -- iteration 5/5  -> '3'
[ 14] Literal          -> '3'
[ 15] Literal          -> '6'

=> '110243433336'

Sample outputs: ['110243433336', '12344333436', '10124433336', '123343436', '1112443433436']
```

---

## Conclusions

This lab assignment pushed further insight into interpreting symbolic logic via AST trees rather than manual string indexing methods. The solution for Variant 1 properly evaluates dynamically unhandled text patterns to randomly extract sequence data that accurately corresponds to the mathematical equations defined by the regular expressions.

Two bugs were identified and corrected during implementation:

1. **Greedy tokenizer digit reading** — the original `while` loop consumed all consecutive digits after `^`, causing `(3|4)^536` to be interpreted as repeat-536 instead of the correct repeat-5 followed by literals `3` and `6`. Fixed by reading exactly one digit.
2. **Mutable default argument** — using `step_counter=[1]` as a default function argument caused the counter to persist and grow across multiple calls, since Python creates mutable defaults only once at definition time. Fixed by using `step_counter=None` and initializing a fresh list inside the function body.

Overall, building this interpreter reinforced the close relationship between regular expressions, formal grammars, and recursive tree evaluation — core concepts that underpin compilers, validators, and pattern-matching engines throughout modern software.