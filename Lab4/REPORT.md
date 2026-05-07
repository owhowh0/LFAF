# Topic: Regular expressions (Variant 1 Alternative)

### Course: Formal Languages & Finite Automata
### Author: Soimu Ionut 

----

## Theory
Regular expressions act as algebraic statements corresponding to regular languages. In everyday scenarios, they serve as templates specifying text patterns that an engine uses algorithmically to match or validate input strings dynamically. Regular Expressions provide extreme versatility with concise syntax to solve complex logical problems involving strings, logs, and compilers. 

The three basic operations of regular expressions—concatenation, union (alternation), and Kleene closure (repetition)—allow an arbitrary combination length of strings to be evaluated smoothly within any data engine configuration.

## Objectives:

1. Write a report detailing regular expressions and their applications.
2. Produce a script interpreting 3 complex expressions conforming to **Variant 1**:
    - `(a|b)(c|d)E^+G?`
    - `P(Q|R|S)T(UV|W|X)*Z^+`
    - `1(0|1)*2(3|4)^536`
3. Dynamically evaluate and process the variants rather than utilizing hard-coded conditions to spawn strings. 
4. Assure unbounded loops (like arbitrary lengths) simulate a randomized bound limited to a max value of 5 times.
5. Create a function tracing the generation processing step-by-step.

## Implementation description

The system operates across three phases designed in pure Python: breaking the string into tokens, converting the tokens into a parse tree, and walking down this tree randomly generating textual values matching variant formulas.

### 1. The Tokenizer Phase
Tokens simplify string operations later. Multi-characters like `^+` translate logically into single actions for the parser. Characters bypass raw string errors. For grouping numerical exponents correctly, `[0-9]` digits are intercepted and grouped back to integer constants to limit exact repetitions on the bounds properly. 

### 2. Node Structuring & Prioritising (AST)
I segregated operations into class blueprints utilizing object inheritance (`RegexNode`), allowing polymorphic recursive descent matching algorithmically in parsing priority: `parse_alt()` -> `parse_concat()` -> `parse_rep()` -> `parse_primary()`. 
```python
def parse_alt(self):
    node = self.parse_concat()
    while self.pos < len(self.tokens) and self.tokens[self.pos] == '|':
        self.pos += 1
        right = self.parse_concat()
        node = Alternation(node, right)
    return node
```
This seamlessly handles multi-branch configurations where expressions like `(UV|W|X)` can resolve smoothly left-to-right via `concat(U, V)` against literal strings.

### 3. Combination Generation Protocol
Once the sequence evaluates down to an Object AST configuration, the `Generator` class launches a generator function that picks paths recursively based on randomizing sequences and bounds limited internally:
```python
elif isinstance(node, Alternation):
    if random.random() < 0.5:
        return self.generate_random(node.left, step_counter)
    else:
        return self.generate_random(node.right, step_counter)
```
For repetition symbols exactly like question marks `?`, it internally casts limits between 0 up to 1. `+` locks `1 to 5`, whilst Kleene stars operate natively inside bounds `0 to 5`.

### Bonus Tracing Implementation
For every variant execution loop, I pass a persistent `step_counter=[]` alongside an explicit `debug` check dynamically traversing downwards. The generator effectively prints matching sequences alongside specific alternation decisions to mimic a programmatic parser reading dynamically sequence-by-sequence.

## Conclusions

This lab assignment pushed further insight into interpreting symbolic logic via AST trees rather than manual string indexing methods. The created solution for Variant 1 properly evaluates dynamically unhandled text patterns to randomly extract sequence data that accurately corresponds to the mathematical equations defined by the regular expressions. The script accurately parsed literal characters mixed effortlessly with strict length multipliers like `^5` and unbounded stars `*` into safe generator loops, producing sets of 100% compliant random strings per formula structure on execution!