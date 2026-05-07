# Topic: Chomsky Normal Form

### Course: Formal Languages & Finite Automata
### Author: Soimu Ionut 

----

## Theory
Chomsky Normal Form (CNF) is a simplified mathematical structure applied to Context-Free Grammars (CFG), playing a crucial role in automata theory and parsing algorithms. In CNF, all production rules are strictly restricted to one of two forms: either a non-terminal produces exactly two non-terminals ($A \rightarrow BC$), or a non-terminal produces exactly one terminal ($A \rightarrow a$). 

This strict binarization format ensures grammatical trees are completely binary. Normalizing CFGs into CNF gives computer scientists robust foundations for polynomial-time parsing algorithms such as the CYK (Cocke-Younger-Kasami) algorithm. Transforming a generic grammar into Chomsky Normal Form requires proceeding logically through specific elimination steps to prevent changing the language recognized while shedding ambiguous structural features like empty string productions or singular variable-to-variable chains.

## Objectives:

1. Learn about Chomsky Normal Form (CNF).
2. Get familiar with the approaches of normalizing a grammar.
3. Implement a method for normalizing an input grammar by the rules of CNF.
    - The implementation needs to be encapsulated in a method with an appropriate signature.
    - The implemented functionality needs executed and tested.
    - Accept any grammar, not only the one from the student's variant (Bonus point).

## Implementation description

The assignment revolves around a standard Context-Free Grammar initialized programmatically. The solution encapsulates the 5 major sequential steps of CNF transformation in individual methods housed in the `Grammar` class. The `to_chomsky_normal_form` function acts as the orchestrator running the exact pipeline necessary to ensure correct resolution.

### 1. Eliminating $\epsilon$-productions
Empty string productions ($\epsilon$) are completely outlawed in strict CNF implementations unless defining the starting state explicitly. My implementation scans the entire set of rules to detect which variables are "nullable" (can potentially generate an empty sequence). Afterward, it iterates over all combinations removing occurrences inside right-hand production sides logically:
```python
nullable_indices = [i for i, char in enumerate(prod) if char in nullable]
for r in range(len(nullable_indices) + 1):
    for combo in itertools.combinations(nullable_indices, r):
        new_prod = "".join([char for i, char in enumerate(prod) if i not in combo])
        if new_prod:
            new_P[nt].add(new_prod)
```

### 2. Eliminating Unit Productions
Unit productions—also known as renamings ($A \rightarrow B$)—serve no purpose other than useless indirection. My script finds direct pairs looping over all possibilities transitively until resolution stagnates. The inner rules of `B` are subsequently copied into the table of `A`, eliminating the necessity to bounce states.

### 3. Eliminating Inaccessible & Non-Productive Symbols
Useless symbols clutter generation and are fundamentally dead logic variables. 
- The algorithm filters **inaccessible symbols** by beginning solely from the `S` (start state) traversing outwards dynamically via right-hand usages. Anything disjointed structurally gets truncated simultaneously.
- **Non-Productive symbols** are scanned looking for variables that successfully resolve strictly to terminal letters ultimately. Using backward evaluation, it maps which abstract letters resolve to real components over iterations. Variables failing to terminate are completely removed.

### 4. Binarizing to Chomsky Normal Form
The final algorithm iterates over existing production sets replacing out-of-order bounds with dynamically generated `X{N}` variables.
It specifically maps singular terminals embedded inside sequences into their own variables immediately. Following that, it dynamically folds rules yielding three or more characters through new intermediate dummy variables until all right-hand targets possess explicitly $2$ symbols max:
```python
for i in range(len(prod) - 2):
    new_var = self.generate_new_var()
    final_P[curr_nt].add(f"{prod[i]}{new_var}")
    curr_nt = new_var
final_P[curr_nt].add(f"{prod[-2]}{prod[-1]}")
```

## Conclusions / Results

Through this laboratory work, I implemented a robust, modular Normalization engine capable of accepting theoretically varied strings of complex Context-Free Grammars (the bonus request) and stripping their unnecessary rules safely. Following sequential structural requirements, the final execution of my script effectively parsed variant 21 mathematically precisely into binary segments ready to be deployed logically for CYK algorithms and tree constructions while logging sequentially readable tables outlining internal adjustments accurately at each step.
