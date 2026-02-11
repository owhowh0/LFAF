import random
from finite_automaton import FiniteAutomaton

class Grammar:

    def __init__(self):
        # Non-terminals
        self.VN = {"S", "B", "D", "Q"}
        
        # Terminals
        self.VT = {"a", "b", "c", "d"}

        # Start symbol
        self.S = "S"

        # Production rules
        self.P = {
            "S": ["aB", "bB"],
            "B": ["cD"],
            "D": ["dQ", "a"],
            "Q": ["bB", "dQ"]
        }

    def generate_string(self):
        current = self.S

        while True:
            replaced = False

            for nt in self.VN:
                if nt in current:
                    production = self.P[nt]
                    chosen = random.choice(production)
                    current = current.replace(nt, chosen, 1)
                    replaced = True
                    break
            
            if not replaced:
                break
        return current
    

    def toFiniteAutomaton(self):
        Q = set(self.VN) 
        Sigma = set(self.VT)
        delta = {}
        F = set()

        for A, productions in self.P.items():
            for production in productions:
                if len(production) == 2:
                    terminal = production[0]
                    non_terminal = production[1]
                    if A not in delta:
                        delta[A] = {}
                    delta[A][terminal] = non_terminal
                elif len(production) == 1:
                    terminal = production
                    F.add(A)
                    if A not in delta:
                        delta[A] = {}
                    delta[A][terminal] = "ACCEPT"

        Q.add("ACCEPT")
        delta["ACCEPT"] = {}

        F.add("ACCEPT")

        return FiniteAutomaton(Q, Sigma, delta, self.S, F)