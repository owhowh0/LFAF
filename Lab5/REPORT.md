# Topic: Chomsky Normal Form (Lab 5)

### Course: Formal Languages & Finite Automata
### Author: Ilie Covali
### Variant: 9

----

This report explains the theoretical background for Chomsky Normal Form and describes how the Lab5 implementation transforms a context-free grammar into CNF. Chomsky Normal Form requires that every production be either a single terminal on the right-hand side or exactly two non-terminals. This constraint is convenient for parsing algorithms such as CYK because it yields binary parse trees and simplifies dynamic programming reasoning.

The first theoretical step in the conversion process is the elimination of epsilon-productions. A non-terminal is nullable if it can derive the empty string. The implementation locates all nullable non-terminals and, for each original production, generates the variants that result from optionally removing nullable symbols from the right-hand side. Explicit epsilon productions are then removed so that the grammar no longer directly produces the empty string, except when handled separately as a special case.

The second theoretical step is the elimination of unit productions, which are productions where a non-terminal produces a single non-terminal. Eliminating unit productions preserves the language by replacing chains of renamings with the eventual non-unit productions of the chain targets. The implementation computes the transitive closure of renaming relations and copies non-unit productions from target variables into origin variables, removing the need for intermediate renamings.

The third theoretical step removes useless symbols. Inaccessible symbols are symbols that cannot be reached from the start symbol; they are found by traversing productions outward from the start symbol and removed. Non-productive symbols are those that cannot derive a terminal string; the implementation marks productive symbols iteratively and removes variables and productions that never lead to terminals.

After the grammar has been pruned, the conversion to CNF proceeds by removing terminals from mixed right-hand sides and by binarizing long right-hand sides. Each terminal that appears inside a right-hand side of length greater than one is replaced by a fresh non-terminal that produces that terminal. Then any production whose right-hand side contains more than two non-terminals is decomposed into a sequence of binary productions by introducing fresh intermediate variables. The fresh variables are named deterministically by the program as `X1`, `X2`, and so on.

The code is organized around the `Grammar` class in `Grammar.py`. The constructor accepts the sets `VN`, `VT`, the productions `P`, and the start symbol `S`. The method `to_chomsky_normal_form()` orchestrates the conversion and calls the following methods in sequence: `eliminate_epsilon_productions()`, `eliminate_renaming()`, `eliminate_inaccessible_symbols()`, `eliminate_non_productive_symbols()`, and `obtain_chomsky_normal_form()`. Each method implements one of the theoretical steps described above and updates the grammar state stored in the instance.

The `eliminate_epsilon_productions()` method computes the nullable set and generates additional productions by omitting nullable symbols where appropriate. The `eliminate_renaming()` method computes unit pairs and copies non-unit productions across them. The `eliminate_inaccessible_symbols()` method performs a reachability traversal from `S`, and `eliminate_non_productive_symbols()` identifies and removes variables that cannot produce terminals. The `obtain_chomsky_normal_form()` method replaces terminals in mixed contexts with fresh variables and breaks down longer productions into binary rules using newly generated intermediate variables.

The driver `main.py` constructs the specific grammar for Variant 9, instantiates `Grammar`, prints the original grammar, runs `to_chomsky_normal_form()`, and prints intermediate and final grammars so the transformation is observable. To reproduce the process, run `python main.py` from the `Lab5` directory; the program prints the grammar before and after each major transformation step and finally prints the grammar in CNF form.

The implementation assumes single-character terminals and non-terminals for the input grammar and uses deterministic naming for generated variables. The resulting grammar is guaranteed to contain only productions of the form `A -> a` or `A -> BC` after the conversion, and the printed output can be inspected to verify correctness. If desired, the report can be extended with a concrete example trace showing how a specific original production is transformed step by step into CNF.

----

End of report.
