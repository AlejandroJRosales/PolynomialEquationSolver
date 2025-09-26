import GeneticAlgorithm

goal = 4

upper_bound = 1
lower_bound = 1
variables  = 2

x = GeneticAlgorithm.solve(goal, upper_bound, lower_bound, variables, n=100, iterations=1000, mutation_mag=.01, print_every=50)
equation = f"(2 ** {x[0]} - 7 + {x[1]}) / 6"

print(f"\nProblem: {goal} = (2 ** x1 - 7 + x2) / 6, solve for variables")
print(f"Computrons Answer: {equation}")
print(f"This computrons answer gives us a solution of {eval(equation)}")
print(f"Error: {abs(goal - eval(equation))}")