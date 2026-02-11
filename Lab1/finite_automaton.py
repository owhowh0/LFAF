class FiniteAutomaton:
    def __init__(self, Q, Sigma, delta, q0, F):
        self.Q = Q  # states
        self.Sigma = Sigma  # alphabet
        self.delta = delta  # transition function
        self.q0 = q0  # initial state
        self.F = F  # final states

    def string_belongs_to_language(self, input_string):
        current_state = self.q0

        for symbol in input_string: 
            if symbol not in self.delta[current_state]:
                return False
            
            current_state = self.delta[current_state][symbol]
        
        return current_state in self.F