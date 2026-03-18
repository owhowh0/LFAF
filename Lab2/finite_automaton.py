from typing import Set, Dict, Tuple, List, Optional
from collections import deque

class FiniteAutomaton:
    """
    Represents a Finite Automaton (both DFA and NDFA)
    """
    def __init__(self, Q: Set[str], Sigma: Set[str], delta: Dict, q0: str, F: Set[str], is_ndfa: bool = False):
        self.Q = Q  # states
        self.Sigma = Sigma  # alphabet
        self.delta = delta  # transition function
        self.q0 = q0  # initial state
        self.F = F  # final states
        self.is_ndfa = is_ndfa

    def is_deterministic(self) -> bool:
        """
        Determine if the automaton is deterministic
        An automaton is non-deterministic if:
        1. There exists a state and symbol with multiple transitions
        2. There are epsilon transitions (not in this implementation)
        """
        for state in self.Q:
            if state not in self.delta:
                continue
            for symbol in self.delta[state]:
                transitions = self.delta[state][symbol]
                # If transition is a list/set, it's NDFA
                if isinstance(transitions, (list, set)):
                    if len(transitions) > 1:
                        return False
        return True

    def string_belongs_to_language_dfa(self, input_string: str) -> bool:
        """
        Check if a string is accepted by the DFA
        """
        current_state = self.q0

        for symbol in input_string:
            if symbol not in self.Sigma:
                return False
            if current_state not in self.delta or symbol not in self.delta[current_state]:
                return False
            
            current_state = self.delta[current_state][symbol]
        
        return current_state in self.F

    def string_belongs_to_language_ndfa(self, input_string: str) -> bool:
        """
        Check if a string is accepted by the NDFA using BFS
        """
        # Start with initial state
        current_states = {self.q0}
        
        for symbol in input_string:
            if symbol not in self.Sigma:
                return False
            
            next_states = set()
            for state in current_states:
                if state in self.delta and symbol in self.delta[state]:
                    transitions = self.delta[state][symbol]
                    if isinstance(transitions, (list, set)):
                        next_states.update(transitions)
                    else:
                        next_states.add(transitions)
            
            current_states = next_states
            if not current_states:
                return False
        
        # Check if any current state is in final states
        return bool(current_states & self.F)

    def string_belongs_to_language(self, input_string: str) -> bool:
        """
        Check if string is accepted - routes to appropriate method
        """
        if self.is_deterministic():
            return self.string_belongs_to_language_dfa(input_string)
        else:
            return self.string_belongs_to_language_ndfa(input_string)

    def to_regular_grammar(self):
        """
        Convert FA to Regular Grammar (Type 3 in Chomsky Hierarchy)
        Returns a Grammar object
        """
        from grammar import Grammar
        
        grammar = Grammar()
        grammar.VN = self.Q.copy()
        grammar.VT = self.Sigma.copy()
        grammar.S = self.q0
        
        # Initialize production rules
        grammar.P = {state: [] for state in self.Q}
        
        # Add transitions as production rules
        for state in self.Q:
            if state in self.delta:
                for symbol in self.delta[state]:
                    transitions = self.delta[state][symbol]
                    
                    if isinstance(transitions, (list, set)):
                        # NDFA case
                        for target_state in transitions:
                            if target_state in self.Q:
                                grammar.P[state].append(symbol + target_state)
                    else:
                        # DFA case
                        if transitions in self.Q:
                            grammar.P[state].append(symbol + transitions)
        
        # Add epsilon productions for final states
        for final_state in self.F:
            grammar.P[final_state].append("ε")
        
        return grammar
