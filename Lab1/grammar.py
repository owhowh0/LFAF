import random


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
    

    def toFiniteAutomaton():
        pass

