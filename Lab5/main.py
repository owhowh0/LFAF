from Grammar import Grammar

def main():
    # Variant 9
    VN = {'S', 'A', 'B', 'C', 'D'}
    VT = {'a', 'b'}
    P = {
        'S': {'bA', 'BC'},
        'A': {'a', 'aS', 'bAaAb'},
        'B': {'A', 'bS', 'aAa'},
        'C': {'epsilon', 'AB'},
        'D': {'AB'}
    }
    S = 'S'

    grammar = Grammar(VN, VT, P, S)
    print("Original Grammar (Variant 9):")
    print(grammar)

    print("\n" + "="*60)
    print("Starting Normalization Process to Chomsky Normal Form (CNF):")
    print("="*60)
    cnf_grammar = grammar.to_chomsky_normal_form()
    print("\nFinal Grammar in Chomsky Normal Form:")
    print(cnf_grammar)


if __name__ == "__main__":
    main()
