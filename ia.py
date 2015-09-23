from bisect import bisect_left
from itertools import izip
from math import hypot, log
from random import shuffle, randrange, random


class Graph(object):

    def __init__(self):
        self.nodes = []
        self.n = 0
        self.distance = []

    def add_node(self, y, x):
        if (y, x) in self.nodes:
            return False
        self.nodes.append((y, x))
        self.n += 1
        self.distance = [[0] * self.n for _ in xrange(self.n)]
        for i, a in enumerate(self.nodes):
            for j, b in enumerate(self.nodes):
                self.distance[i][j] = hypot(a[0] - b[0], a[1] - b[1])
        return True

    def solve(self):
        if self.n > 1:
            solver = GeneticSolver(self)
            order = solver.solve()
            solution = []
            for a, b in izip(order, order[1:]):
                solution.append((self.nodes[a], self.nodes[b]))
            solution.append((self.nodes[order[-1]], self.nodes[order[0]]))
            return solution
        return []


class GeneticSolver(object):

    def __init__(self, graph):
        self.graph = graph

    def get_random_population(self, population_size):
        population = []
        for _ in xrange(population_size):
            individual = range(self.graph.n)
            shuffle(individual)
            population.append(individual)
        return population

    def measure(self, individual):
        cost = 0
        for a, b in izip(individual, individual[1:]):
            cost += self.graph.distance[a][b]
        cost += self.graph.distance[individual[-1]][individual[0]]
        return 1. / cost

    @staticmethod
    def mutate(individual):
        a = randrange(len(individual))
        b = randrange(len(individual))
        while b == a:
            b = randrange(len(individual))
        if b < a:
            a, b = b, a
        return individual[:a] + [individual[b]] + [individual[a]] + \
            individual[a+1:b] + individual[b+1:]

    @staticmethod
    def crossover(ind1, ind2):
        n = len(ind1)
        child1, child2 = [], []
        for i in xrange(n):
            if random() > 0.8:
                child1.append(ind2[i])
                child2.append(ind1[i])
            else:
                child1.append(-1)
                child2.append(-1)
        i = 0
        for x in ind1:
            if x in child1:
                continue
            while child1[i] != -1:
                i += 1
            child1[i] = x
        i = 0
        for x in ind2:
            if x in child2:
                continue
            while child2[i] != -1:
                i += 1
            child2[i] = x
        return child1, child2

    def get_fitness(self, population):
        return [self.measure(ind) for ind in population]

    @staticmethod
    def get_distribution(costs):
        total = sum(costs)
        acc = 0
        distribution = []
        for cost in costs:
            acc += cost / total
            distribution.append(acc)
        return distribution

    @staticmethod
    def get_best(population, fitness, k=1):
        if k == 1:
            return max(zip(fitness, population))[1]
        return [x for _, x in sorted(zip(fitness, population),
                                     reverse=True)][:k]

    @staticmethod
    def get_random_individual(population, distribution):
        return population[bisect_left(distribution, random())]

    def solve(self, iterations=400, population_size=50):
        population = self.get_random_population(population_size)
        fitness = self.get_fitness(population)
        for _ in xrange(iterations):
            next_population = self.get_best(population, fitness,
                                            int(log(population_size)) + 1)
            distribution = self.get_distribution(fitness)
            random_args = (population, distribution)

            while len(next_population) < population_size:
                if random() < 0.2:
                    next_population.append(
                        self.mutate(self.get_random_individual(*random_args)))
                else:
                    next_population.extend(
                        self.crossover(
                            self.get_random_individual(*random_args),
                            self.get_random_individual(*random_args)))
            if len(next_population) > population_size:
                next_population.pop(randrange(len(next_population)))

            population = next_population
            fitness = self.get_fitness(population)

        return self.get_best(population, fitness)
