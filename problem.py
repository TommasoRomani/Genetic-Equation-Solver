from time import sleep
from population import Population
import numpy as np
import random
from utils import *
import copy

#definition of the problem class and its methods
class Problem:

    def __init__(self, pop_size, num_gen, result):
        self.pop_size = pop_size
        self.num_gen = num_gen
        self.result = result
        self.population = Population(self.pop_size, 3 , 10)

    def evolve(self, p_mutation, max_depth):
        self.population.initialize()
        for i in range(self.num_gen):
            #print('starting population size: ' + str(len(self.population.population)) + ' individuals')
            print("Generation: " + str(i))

            # select mating pool
            mating_pool = self.population.select_pool(self.pop_size)
            print(len(mating_pool))
            for elem in mating_pool:
                # apply crossover with prob 1-p_mutation
                if random.random() > p_mutation:
                    if len(mating_pool) >= 2:  # Ensure there are at least 2 elements in the mating pool
                        p1,p2 = np.random.choice(mating_pool, size=(2), replace=False)
                        self.population.crossover(p1,p2, max_depth)
                        mating_pool.remove(p1)
                        mating_pool.remove(p2)
                    else:
                        continue
                # apply mutation with prob p_mutation
                else:
                    # apply mutation
                    pm = np.random.choice(mating_pool, size=1)[0]
                    self.population.mutation(pm, max_depth)
                    mating_pool.remove(pm)
            # evaluate
            # select new population
            
            evaluated = self.population.calculate_fitness(self.result)
            # computes best elements form evaluated
            evaluated = sorted(evaluated, key=lambda x: x[1])
            #for element in evaluated:
            #    print(f"element has fitness of {element[0].evaluate()} and evaluates to {element[1]}")
            pop , fitness = zip(*evaluated)
            # selection by removing worst elements
            for i in range(len(pop)-self.pop_size):
                # remove worst elements
                pop = pop[:-1]
                fitness = fitness[:-1]
            # update population
            del self.population.population[:]
            self.population.population = copy.deepcopy(list(pop))
            
            print("Best: " + str(self.population.population[0].evaluate()))
            sleep(1)
            
            # check if best element is similar to result
            if (self.population.population[0].evaluate() < (self.result +100)) and (self.population.population[0].evaluate() > (self.result -100)) :
            #if self.population.population[0].evaluate() == self.result:
                print("Good Solution found in generation: " + str(i))
                print("Solution: " + str(self.population.population[0]))
                break
        self.population.best()
                    
            # evaluate each element and apply selection
        