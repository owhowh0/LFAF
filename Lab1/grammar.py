class Grammar:

    def __init__(self):
        self.VN = {"S", "B", "D", "Q"}

        self.VT = {"a", "b", "c", "d"}

        self.S = "S"

        self.P = {
            "S": ["aB", "bB"],
            "B": ["cD"],
            "D": ["dQ", "a"],
            "Q": ["bB", "dQ"]
        }

    def generate_string():
        pass

    def toFiniteAutomaton():
        pass

