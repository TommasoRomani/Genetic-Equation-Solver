from time import sleep
from population import Population
import numpy as np
import random
import pandas as pd
import copy
import heapq


class Problem:

    def __init__(self, pop_size:int, num_gen:int, equation_name:str):
        self.pop_size = pop_size
        self.num_gen = num_gen
        self.data = pd.read_csv(f'{equation_name}.csv',sep=';').to_dict('records')
        self.population = Population(self.pop_size, 1 , 3, self.data)


    def evolve(self, p_mutation:float, depth_penalty:int, max_depth, selction_method:str):
        """
        Evolves the population over a number of generations.

        Parameters:
        - p_mutation (float): The probability of mutation.
        - depth_penalty (int): The penalty for exceeding the maximum depth.
        - max_depth (int): The maximum depth of the individuals.
        - selction_method (str): The selection method to use.

        Returns:
        - Individual: The best individual found after evolution.
        """
        self.population.initialize()
        for i in range(self.num_gen):
            offspring_count = 0
            print("Generation: " + str(i))

            # select mating pool
            self.population.calculate_fitness(self.population.population ,self.data, depth_penalty, max_depth)
            self.population.population = sorted(self.population.population, key=lambda x:x.fitness)
            if selction_method == 'overselction':
                self.population.parents = self.population.overselection(self.pop_size, self.population.population)
            else:
                self.population.parents = self.population.stochastic_universal_sampling(self.pop_size//2, self.population.population)
            
            # variation operations (crossover and mutation)
            while len(self.population.offspring) <= 10*self.pop_size:
                # apply crossover with prob 1-p_mutation
                if random.random() > p_mutation:
                        if len(self.population.parents) > 1:
                            p1,p2 = np.random.choice(self.population.parents, size=(2), replace=False)
                            self.population.crossover(p1, p2, max_depth,depth_penalty)
                        # if there is only one parent, apply mutation
                        else:
                            pm = np.random.choice(self.population.parents, size=1)[0]
                            self.population.mutation(pm, max_depth ,depth_penalty)
                else:
                    # apply mutation with prob p_mutation
                    pm = np.random.choice(self.population.parents, size=1)[0]
                    self.population.mutation(pm, max_depth ,depth_penalty)

       
            # applies (mu, lambda) selection
            self.population.population = heapq.nsmallest(self.pop_size, self.population.offspring, key=lambda x: x.fitness)
            # deletes the offspring list for the next generation
            del self.population.offspring[:]
            best = min(self.population.population, key=lambda x: x.fitness)
            print(f"Best value {best.value} found until now")
            print(best)

            # stops early if the integer part of fitness is 0
            if best.fitness == np.inf:
                continue
            if int(best.value) == 0:
                print(f"Final equation found = {best} \n in {i} generations with vvalue {best.value}")
                return best
        self.population.population = sorted(self.population.population, key=lambda x:x.fitness)
        print(f"Final equation found = {self.population.population[0]}")
        print(self.population.population[0].fitness)
        return self.population.population[0]
        