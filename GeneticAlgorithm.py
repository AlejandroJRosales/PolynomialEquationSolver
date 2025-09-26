import random

tournament_size = 3
pop_keep = .85
prob_crossover = 0.8
prob_mutation = 0.15


def generate_population(lower_bound, upper_bound, genes_per_ch, n):
        return [[random.randint(lower_bound, upper_bound) + random.random() for c in range(0, genes_per_ch)] for i in range(0, n)]


def calc_fitness(goal, population, lower_bound, upper_bound):
        return [abs(goal - float((2 ** individual[0] - 7 + individual[1])) / 6) for individual in population]


def select_fittest(population, fitness_scores, lower_bound, upper_bound, genes_per_ch):
        n = len(population)
        fitter_population = []
        for _ in range(int(n * pop_keep)):
                r = random.randint(0, n - 1)
                best_fitness, best_individual = fitness_scores[r], population[r]
                for member in range(tournament_size):
                        competitor_index = random.randint(0, n - 1)
                        if fitness_scores[competitor_index] < best_fitness:
                                best_fitness = fitness_scores[competitor_index]
                                best_individual = population[competitor_index]
                fitter_population.append(best_individual)

        fitter_population += generate_population(lower_bound, upper_bound, genes_per_ch, n - len(fitter_population))

        return fitter_population


def crossover(population, genes_per_ch):
        for index in range(0, len(population), 2):
                if random.random() <= prob_crossover:
                        individual1 = population[index]
                        individual2 = population[index + 1]
                        r = random.randint(0, genes_per_ch)
                        population[index] = individual1[:r] + individual2[r:]
                        population[index + 1] = individual2[:r] + individual1[r:]

        return population


def mutation(population, genes_per_ch, mutation_mag):
    for index in range(len(population)):
          individual = population[index]
          for ch in range(genes_per_ch):
              if random.random() <= prob_mutation:
                gene = individual[ch]
                if random.random() < 0.5:
                    individual[ch] = gene + (gene * mutation_mag)
                else:
                    individual[ch] = gene - (gene * mutation_mag)
          
          population[index] = individual

    return population


def breed(population, genes_per_ch, mutation_mag):
        return mutation(crossover(population, genes_per_ch), genes_per_ch, mutation_mag)


def solve(goal, lower_bound, upper_bound, genes_per_ch, n=250, iterations=250, mutation_mag=.001, print_every=50):
        population = generate_population(lower_bound, upper_bound, genes_per_ch, n)
        variables = []
        abs_best = 10000
        variables = []
        for generation in range(0, iterations + 1):
                pop_fitness = calc_fitness(goal, population, lower_bound, upper_bound)
                if (generation % print_every == 0) | (pop_fitness[pop_fitness.index(min(pop_fitness))] == 0):
                        best = min(pop_fitness)
                        if best < abs_best:
                              abs_best = best
                              variables = population[pop_fitness.index(best)]
                        mode = max(set(pop_fitness), key=pop_fitness.count)
                        worst = max(pop_fitness)
                        print("[G %3d] score=(%.10f, %.3f, %.3f): %r" %
                              (generation, best, mode, worst, population[pop_fitness.index(best)]))
                        if best == 0:
                                break
                population = breed(select_fittest(population, pop_fitness, lower_bound, upper_bound, genes_per_ch), genes_per_ch, mutation_mag)
        
        return variables
