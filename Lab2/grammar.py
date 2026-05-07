from typing import Set, Dict, List, Optional
from enum import Enum

class ChomskyType(Enum):
    TYPE_0 = "Type 0 (Unrestricted)"
    TYPE_1 = "Type 1 (Context-Sensitive)"
    TYPE_2 = "Type 2 (Context-Free)"
    TYPE_3 = "Type 3 (Regular)"
    INVALID = "Invalid"

class Grammar:

    def __init__(self):
        self.VN = set()  # Non-terminals
        self.VT = set()  # Terminals
        self.S = None  # Start symbol
        self.P = {}  # Production rules {non_terminal: [productions]}

    def set_rules(self, VN: Set[str], VT: Set[str], S: str, P: Dict[str, List[str]]):
        self.VN = VN
        self.VT = VT
        self.S = S
        self.P = P

    def classify_chomsky_hierarchy(self) -> ChomskyType:        
        if not self.P:
            return ChomskyType.INVALID
        
        is_regular = True
        is_context_free = True
        is_context_sensitive = True
        
        for lhs, productions in self.P.items():
            # Check if left side is single non-terminal
            if not isinstance(lhs, str):
                is_context_free = False
                is_regular = False
                continue
            
            for rhs in productions:
                if is_regular:
                    if rhs == "ε":
                        pass
                    elif len(rhs) == 1 and rhs in self.VT:
                        pass
                    elif len(rhs) >= 2:
                        first_char = rhs[0]
                        rest = rhs[1:]
                        if first_char in self.VT and rest in self.VN:
                            pass
                        else:
                            is_regular = False
                    else:
                        is_regular = False
                
                if is_context_sensitive:
                    if rhs != "ε":
                        if len(lhs) > len(rhs):
                            is_context_sensitive = False
        
        if is_regular:
            return ChomskyType.TYPE_3
        elif is_context_free:
            return ChomskyType.TYPE_2
        elif is_context_sensitive:
            return ChomskyType.TYPE_1
        else:
            return ChomskyType.TYPE_0

    def __str__(self) -> str:
        result = "Grammar:\n"
        result += f"VN (Non-terminals): {self.VN}\n"
        result += f"VT (Terminals): {self.VT}\n"
        result += f"S (Start symbol): {self.S}\n"
        result += "P (Productions):\n"
        for nt, prods in self.P.items():
            result += f"  {nt} → {' | '.join(prods)}\n"
        return result
