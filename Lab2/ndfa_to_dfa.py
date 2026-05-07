from typing import Set, Dict
from finite_automaton import FiniteAutomaton

class NDFAToDFAConverter:
    def __init__(self, ndfa: FiniteAutomaton):
        self.ndfa = ndfa
        self.dfa = None
        self.state_mapping = {}  # Maps frozenset of NDFA states to DFA state name

    def convert(self) -> FiniteAutomaton:
        # Normalize NDFA transitions to use sets
        normalized_delta = self.normalize_transitions()
        
        # Start with the initial state
        dfa_states = set()
        dfa_delta = {}
        dfa_initial = frozenset([self.ndfa.q0])
        
        # Queue for BFS
        unprocessed = [dfa_initial]
        dfa_states.add(dfa_initial)
        state_counter = 0
        
        # Create mapping for state names
        state_names = {}
        state_names[dfa_initial] = f"q{state_counter}"
        self.state_mapping[dfa_initial] = f"q{state_counter}"
        state_counter += 1
        
        # Process each subset of NDFA states
        while unprocessed:
            current_subset = unprocessed.pop(0)
            current_state_name = state_names[current_subset]
            dfa_delta[current_state_name] = {}
            
            # For each symbol in alphabet
            for symbol in self.ndfa.Sigma:
                next_states = set()
                
                # Find all states reachable from current subset on this symbol
                for state in current_subset:
                    if state in normalized_delta and symbol in normalized_delta[state]:
                        next_states.update(normalized_delta[state][symbol])
                
                if next_states:
                    next_subset = frozenset(next_states)
                    
                    # Add to DFA transitions
                    if next_subset not in state_names:
                        state_names[next_subset] = f"q{state_counter}"
                        self.state_mapping[next_subset] = f"q{state_counter}"
                        state_counter += 1
                        dfa_states.add(next_subset)
                        unprocessed.append(next_subset)
                    
                    dfa_delta[current_state_name][symbol] = state_names[next_subset]
        
        # Determine final states in DFA
        # A DFA state is final if it contains at least one final state from NDFA
        dfa_final_states = set()
        for subset, name in state_names.items():
            if subset & self.ndfa.F:  # Intersection with final states
                dfa_final_states.add(name)
        
        # Create DFA state set with named states
        dfa_state_set = set(state_names.values())
        dfa_initial_name = state_names[dfa_initial]
        
        # Create and return DFA
        self.dfa = FiniteAutomaton(
            Q=dfa_state_set,
            Sigma=self.ndfa.Sigma,
            delta=dfa_delta,
            q0=dfa_initial_name,
            F=dfa_final_states,
            is_ndfa=False
        )
        
        return self.dfa

    def normalize_transitions(self) -> Dict[str, Dict[str, Set[str]]]:
        normalized = {}
        
        for state in self.ndfa.Q:
            normalized[state] = {}
            
            if state not in self.ndfa.delta:
                continue
            
            for symbol in self.ndfa.delta[state]:
                target = self.ndfa.delta[state][symbol]
                
                if isinstance(target, set):
                    normalized[state][symbol] = target.copy()
                elif isinstance(target, list):
                    normalized[state][symbol] = set(target)
                else:
                    normalized[state][symbol] = {target}
        
        return normalized

    def get_conversion_report(self) -> str:
        if not self.dfa:
            return "Conversion not yet performed"
        
        report = "NDFA to DFA Conversion Report\n"
        
        report += "Original NDFA:\n"
        report += f"  States (Q): {self.ndfa.Q}\n"
        report += f"  Alphabet (Σ): {self.ndfa.Sigma}\n"
        report += f"  Initial state (q0): {self.ndfa.q0}\n"
        report += f"  Final states (F): {self.ndfa.F}\n"
        report += f"  Transitions:\n"
        for state in sorted(self.ndfa.Q):
            if state in self.ndfa.delta:
                for symbol in sorted(self.ndfa.delta[state]):
                    targets = self.ndfa.delta[state][symbol]
                    if isinstance(targets, (set, list)):
                        for target in targets:
                            report += f"    δ({state}, {symbol}) = {target}\n"
                    else:
                        report += f"    δ({state}, {symbol}) = {targets}\n"
        
        report += "\nConverted DFA:\n"
        report += f"  States (Q'): {self.dfa.Q}\n"
        report += f"  Alphabet (Σ): {self.dfa.Sigma}\n"
        report += f"  Initial state (q0'): {self.dfa.q0}\n"
        report += f"  Final states (F'): {self.dfa.F}\n"
        report += f"  Transitions:\n"
        for state in sorted(self.dfa.Q):
            if state in self.dfa.delta:
                for symbol in sorted(self.dfa.delta[state]):
                    target = self.dfa.delta[state][symbol]
                    report += f"    δ({state}, {symbol}) = {target}\n"
        
        report += f"\nState Mapping (NDFA subset → DFA state):\n"
        for ndfa_subset in sorted(self.state_mapping.keys(), key=lambda x: self.state_mapping[x]):
            dfa_state = self.state_mapping[ndfa_subset]
            report += f"  {set(ndfa_subset)} → {dfa_state}\n"
        
        report += f"\nNumber of states: NDFA = {len(self.ndfa.Q)}, DFA = {len(self.dfa.Q)}\n"
        
        return report
