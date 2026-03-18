from finite_automaton import FiniteAutomaton

class AutomatonVisualizer:    
    def __init__(self, fa: FiniteAutomaton):
        self.fa = fa

    def to_dot(self) -> str:
        """
        Generate a Graphviz DOT representation of the automaton
        """
        dot = "digraph FA {\n"
        dot += "  rankdir=LR;\n"
        dot += "  size=\"8,6\";\n"
        dot += "  node [shape=circle];\n"
        
        # Add initial state indicator
        dot += "  _start [shape=point];\n"
        dot += f"  _start -> {self.fa.q0};\n"
        
        # Mark final states with double circles
        for final_state in self.fa.F:
            dot += f"  {final_state} [shape=doublecircle];\n"
        
        # Add transitions
        transitions_dict = {}  # Group transitions between same pair of states
        
        for from_state in sorted(self.fa.Q):
            if from_state not in self.fa.delta:
                continue
            
            for symbol in sorted(self.fa.delta[from_state]):
                targets = self.fa.delta[from_state][symbol]
                
                if isinstance(targets, (set, list)):
                    for to_state in sorted(targets):
                        key = (from_state, to_state)
                        if key not in transitions_dict:
                            transitions_dict[key] = []
                        transitions_dict[key].append(symbol)
                else:
                    to_state = targets
                    key = (from_state, to_state)
                    if key not in transitions_dict:
                        transitions_dict[key] = []
                    transitions_dict[key].append(symbol)
        
        # Write transitions with combined labels
        for (from_state, to_state), symbols in sorted(transitions_dict.items()):
            label = ",".join(sorted(symbols))
            dot += f"  {from_state} -> {to_state} [label=\"{label}\"];\n"
        
        dot += "}\n"
        return dot

    def save_dot(self, filename: str) -> None:
        """
        Save the DOT representation to a file
        """
        with open(filename, 'w') as f:
            f.write(self.to_dot())
        print(f"Saved DOT representation to {filename}")

    def to_mermaid(self) -> str:
        """
        Generate a Mermaid diagram representation
        """
        mermaid = "graph LR\n"
        
        # Add initial state
        mermaid += "  [*] --> " + self.fa.q0 + "\n"
        
        # Group transitions
        transitions_dict = {}
        
        for from_state in sorted(self.fa.Q):
            if from_state not in self.fa.delta:
                continue
            
            for symbol in sorted(self.fa.delta[from_state]):
                targets = self.fa.delta[from_state][symbol]
                
                if isinstance(targets, (set, list)):
                    for to_state in sorted(targets):
                        key = (from_state, to_state)
                        if key not in transitions_dict:
                            transitions_dict[key] = []
                        transitions_dict[key].append(symbol)
                else:
                    to_state = targets
                    key = (from_state, to_state)
                    if key not in transitions_dict:
                        transitions_dict[key] = []
                    transitions_dict[key].append(symbol)
        
        # Write transitions
        for (from_state, to_state), symbols in sorted(transitions_dict.items()):
            label = ",".join(sorted(symbols))
            mermaid += f"  {from_state} --> |{label}| {to_state}\n"
        
        # Mark final states
        for final_state in sorted(self.fa.F):
            mermaid += f"  {final_state} --> [*]\n"
        
        return mermaid

    def __str__(self) -> str:
        """Return the DOT representation"""
        return self.to_dot()
