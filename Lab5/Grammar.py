import itertools
import copy

class Grammar:
    def __init__(self, VN, VT, P, S):
        self.VN = set(VN)
        self.VT = set(VT)
        # Ensure P values are sets
        self.P = {k: set(v) if not isinstance(v, set) else v for k, v in P.items()}
        self.S = S
        self.new_vars_count = 1

    def generate_new_var(self):
        """Generate a new variable name that doesn't exist in VN."""
        while f"X{self.new_vars_count}" in self.VN:
            self.new_vars_count += 1
        var = f"X{self.new_vars_count}"
        self.VN.add(var)
        self.new_vars_count += 1
        return var

    def eliminate_epsilon_productions(self):
        """Step 1: Eliminate ε (epsilon) productions."""
        print("  Step 1.1: Finding nullable non-terminals...")
        
        # Find all nullable non-terminals
        nullable = set()
        
        # First pass: directly nullable
        for nt, prods in self.P.items():
            if 'epsilon' in prods:
                nullable.add(nt)
        
        # Iterative pass: indirect nullable
        changed = True
        while changed:
            changed = False
            for nt, prods in self.P.items():
                if nt not in nullable:
                    for prod in prods:
                        if prod != 'epsilon' and len(prod) > 0:
                            # Check if all symbols in production are nullable
                            all_nullable = True
                            for char in prod:
                                if char not in nullable:
                                    all_nullable = False
                                    break
                            if all_nullable:
                                nullable.add(nt)
                                changed = True
                                break
        
        print(f"  Nullable non-terminals: {nullable}")
        
        # Generate new productions from nullable non-terminals
        new_P = {nt: set() for nt in self.P.keys()}
        
        for nt, prods in self.P.items():
            for prod in prods:
                if prod != 'epsilon':
                    new_P[nt].add(prod)
                    
                    # Find positions of nullable symbols
                    nullable_pos = [i for i, char in enumerate(prod) if char in nullable]
                    
                    # Generate all subsets by removing nullable symbols
                    for r in range(1, len(nullable_pos) + 1):
                        for positions in itertools.combinations(nullable_pos, r):
                            new_prod = ''.join([char for i, char in enumerate(prod) if i not in positions])
                            if new_prod:  # Only add non-empty productions
                                new_P[nt].add(new_prod)
        
        # Remove epsilon productions
        for nt in new_P:
            if 'epsilon' in new_P[nt]:
                new_P[nt].discard('epsilon')
        
        self.P = new_P
        print(f"  After eliminating epsilon: {self}")

    def eliminate_renaming(self):
        """Step 2: Eliminate unit productions (A -> B where B is non-terminal)."""
        print("  Step 2.1: Finding unit production chains...")
        
        # Find all unit production pairs
        unit_pairs = set()
        for nt in self.VN:
            unit_pairs.add((nt, nt))
        
        # Closure: if A -> B and B -> C then A -> C
        changed = True
        while changed:
            changed = False
            new_pairs = set()
            for A, B in list(unit_pairs):
                if B in self.P:
                    for prod in self.P[B]:
                        if len(prod) == 1 and prod in self.VN:
                            if (A, prod) not in unit_pairs:
                                new_pairs.add((A, prod))
                                changed = True
            unit_pairs.update(new_pairs)
        
        # Build new productions
        new_P = {nt: set() for nt in self.VN}
        
        for A, B in unit_pairs:
            if B in self.P:
                for prod in self.P[B]:
                    # Only add if it's not a unit production
                    if not (len(prod) == 1 and prod in self.VN):
                        new_P[A].add(prod)
        
        self.P = {nt: prods for nt, prods in new_P.items() if prods}
        print(f"  After eliminating unit productions: {self}")

    def eliminate_inaccessible_symbols(self):
        """Step 3: Eliminate inaccessible symbols."""
        print("  Step 3.1: Finding accessible symbols from start symbol...")
        
        # BFS from start symbol
        accessible = {self.S}
        queue = [self.S]
        
        while queue:
            nt = queue.pop(0)
            if nt in self.P:
                for prod in self.P[nt]:
                    for char in prod:
                        if char in self.VN and char not in accessible:
                            accessible.add(char)
                            queue.append(char)
        
        print(f"  Accessible symbols: {accessible}")
        
        # Remove inaccessible symbols
        self.VN = self.VN.intersection(accessible)
        self.P = {nt: prods for nt, prods in self.P.items() if nt in accessible}
        print(f"  After eliminating inaccessible symbols: {self}")

    def eliminate_non_productive_symbols(self):
        """Step 4: Eliminate non-productive symbols."""
        print("  Step 4.1: Finding productive symbols...")
        
        # Find productive symbols
        productive = set()
        changed = True
        
        while changed:
            changed = False
            for nt, prods in self.P.items():
                if nt not in productive:
                    for prod in prods:
                        # A production is productive if all symbols are terminals or productive non-terminals
                        is_productive = True
                        for char in prod:
                            if char in self.VN and char not in productive:
                                is_productive = False
                                break
                        if is_productive:
                            productive.add(nt)
                            changed = True
                            break
        
        print(f"  Productive symbols: {productive}")
        
        # Remove non-productive symbols
        self.VN = self.VN.intersection(productive)
        
        # Remove productions containing non-productive symbols
        new_P = {}
        for nt in self.VN:
            if nt in self.P:
                valid_prods = set()
                for prod in self.P[nt]:
                    valid = True
                    for char in prod:
                        if char in self.VN and char not in productive:
                            valid = False
                            break
                    if valid:
                        valid_prods.add(prod)
                if valid_prods:
                    new_P[nt] = valid_prods
        
        self.P = new_P
        print(f"  After eliminating non-productive symbols: {self}")

    def obtain_chomsky_normal_form(self):
        """Step 5: Convert to Chomsky Normal Form."""
        print("  Step 5.1: Converting to CNF...")
        
        # Phase 1: Replace terminals in multi-symbol productions
        terminal_to_var = {}
        new_P = {}
        
        for nt in self.P.keys():
            new_P[nt] = set()
        
        for nt, prods in self.P.items():
            for prod in prods:
                if len(prod) == 1:
                    new_P[nt].add(prod)
                else:
                    # Parse production and replace terminals
                    symbols = []
                    for char in prod:
                        if char in self.VT:
                            if char not in terminal_to_var:
                                var = self.generate_new_var()
                                terminal_to_var[char] = var
                                new_P[var] = {char}  # Add terminal production
                            symbols.append(terminal_to_var[char])
                        else:
                            symbols.append(char)
                    
                    new_P[nt].add(''.join(symbols))
        
        # Ensure all terminal variables are in new_P
        for term, var in terminal_to_var.items():
            if var not in new_P:
                new_P[var] = {term}
            elif term not in new_P[var]:
                new_P[var].add(term)
        
        # Phase 2: Break down productions longer than 2 symbols
        final_P = {}
        for nt in new_P:
            final_P[nt] = set()
        
        for nt, prods in new_P.items():
            for prod in prods:
                if len(prod) <= 2:
                    final_P[nt].add(prod)
                else:
                    # Parse to identify symbols (single-char or X##)
                    symbols = []
                    i = 0
                    while i < len(prod):
                        if prod[i] == 'X':
                            j = i + 1
                            while j < len(prod) and prod[j].isdigit():
                                j += 1
                            symbols.append(prod[i:j])
                            i = j
                        else:
                            symbols.append(prod[i])
                            i += 1
                    
                    # Break into pairs
                    current_nt = nt
                    for idx in range(len(symbols) - 2):
                        new_var = self.generate_new_var()
                        final_P[current_nt].add(symbols[idx] + new_var)
                        current_nt = new_var
                        if current_nt not in final_P:
                            final_P[current_nt] = set()
                    
                    final_P[current_nt].add(symbols[-2] + symbols[-1])
        
        self.P = final_P
        print(f"  After CNF conversion: {self}")

    def to_chomsky_normal_form(self):
        """Convert the grammar to Chomsky Normal Form through all steps."""
        print("1. Eliminating ε-productions...")
        self.eliminate_epsilon_productions()
        
        print("\n2. Eliminating unit productions (renaming)...")
        self.eliminate_renaming()
        
        print("\n3. Eliminating inaccessible symbols...")
        self.eliminate_inaccessible_symbols()
        
        print("\n4. Eliminating non-productive symbols...")
        self.eliminate_non_productive_symbols()
        
        print("\n5. Obtaining Chomsky Normal Form...")
        self.obtain_chomsky_normal_form()
        
        return self

    def __str__(self):
        if not self.P:
            return "Empty grammar"
        
        p_list = []
        for k in sorted(self.P.keys()):
            v = self.P[k]
            prods = ' | '.join(sorted(v))
            p_list.append(f"{k} -> {prods}")
        
        p_str = "\n  ".join(p_list)
        return f"VN: {sorted(self.VN)}\nVT: {sorted(self.VT)}\nP:\n  {p_str}\nS: {self.S}"

