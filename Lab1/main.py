from grammar import Grammar


g = Grammar()

print("Generated strings:")
for _ in range(5):
    print(g.generate_string())