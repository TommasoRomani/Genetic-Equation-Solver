from math import nan
import random
from tree import Tree
import numpy as np
from time import sleep
import copy
import math
from concurrent.futures import ProcessPoolExecutor




class Population:

    def __init__(self, population_size, min_depth ,max_depth, data):
        self.population_size = population_size
        self.max_depth = max_depth
        self.min_depth = min_depth
        self.population = []
        self.parents = []
        self.offspring = []
        self.data = data
        
    def initialize(self):
        """
        Initializes the population by creating and adding trees to the population list.

        Each tree is created using the ramped half-and-half method with a random depth
        between `min_depth` and `max_depth`.

        Parameters:
            None

        Returns:
            None
        """
        for i in range(self.population_size):
            t = Tree()
            t.ramped_half_and_half(random.randint(self.min_depth, self.max_depth))
            self.population.append(t)
        

    def fitness_distribution(self, s, population):
            """
            Calculate the fitness distribution of a population.

            Parameters:
            s (float): Selection pressure.
            population (list): List of individuals in the population.

            Returns:
            numpy.ndarray: Cumulative sum of the fitness distribution.
            """
            p_rank=[]
            mu = len(population)
            for i,element in enumerate(population):
                p_rank.append(((2-s)/mu) + (((2*(mu-i-1))*(s-1))/(mu*(mu-1))))
                
            return np.cumsum(p_rank)


    def stochastic_universal_sampling(self, offspring_size, population):
        """
        Performs stochastic universal sampling to select individuals from the population for mating.

        Args:
            offspring_size (int): The number of individuals to select for the mating pool.
            population (list): The current population of individuals.

        Returns:
            list: The selected individuals for mating.
        """
        current = 1
        i = 0
        r = random.uniform(0, 1 / offspring_size)
        a = self.fitness_distribution(1, population)
        mating_pool = []
        while current <= offspring_size:
            while r <= a[i]:
                mating_pool.append(population[i])
                r += 1 / offspring_size
                current += 1
            i += 1
        return mating_pool
    

    def overselection(self, offspring_size, population):
            """
            Perform overselection to select offspring from a very large population.

            Args:
                offspring_size (int): The desired size of the offspring.
                population (list): The population from which to select offspring.

            Returns:
                list: The selected offspring.

            """
            # Determine the cutoff for the top 20% of the population
            cutoff = int(0.2 * len(population))

            # Split the population into the top 20% and the bottom 80%
            top_20 = population[:cutoff]
            bottom_80 = population[cutoff:]

            # Select 80% of the offspring from the top 20% of the population
            top_offspring = self.stochastic_universal_sampling(int(0.8 * offspring_size), top_20)

            # Select 20% of the offspring from the bottom 80% of the population
            bottom_offspring = self.stochastic_universal_sampling(offspring_size - len(top_offspring), bottom_80)

            # Combine the offspring from the top 20% and the bottom 80%
            return top_offspring + bottom_offspring
   

    def crossover(self, p1, p2, max_depth ,depth_penalty):
        """
        Performs crossover operation between two individuals.

        Args:
            p1 (Individual): The first parent individual.
            p2 (Individual): The second parent individual.
            max_depth (int): The maximum depth of the individuals.
            depth_penalty (float): The penalty for exceeding the maximum depth.

        Returns:
            None
        """
        p_1 = copy.deepcopy(p1)
        p_2 = copy.deepcopy(p2)

        s1 = p_1.random_subtree()
        s2 = p_2.random_subtree()

        p_1 = p_1.swap_subtree(s1, s2)
        p_2 = p_2.swap_subtree(s2, s1)

        self.single_element_fitness(p_1, self.data, depth_penalty, max_depth)
        self.single_element_fitness(p_2, self.data, depth_penalty, max_depth)
        
        self.offspring.append(p_1)
        self.offspring.append(p_2)


    def mutation(self, p, max_depth, depth_penalty):
        """
        Mutates an individual in the population.

        Parameters:
        p (Tree): The individual to be mutated.
        max_depth (int): The maximum depth of the individual.
        depth_penalty (float): The penalty for exceeding the maximum depth.

        Returns:
        None
        """
        p_m = copy.deepcopy(p)
        s = p_m.random_subtree()
        m = Tree()
        m.ramped_half_and_half(random.randint(1, 3))
        p_m.swap_subtree(s, m)

        self.single_element_fitness(p_m, self.data, depth_penalty, max_depth)
        
        self.offspring.append(p_m) 

    
    def calculate_fitness(self, population, data, depth_penalty, max_depth):
            """
            Calculates the fitness of each element in the population using parallel processing.
            
            Args:
                population (list): List of elements to calculate fitness for.
                data (list): Data used for fitness calculation.
                depth_penalty (float): Penalty factor for depth of elements.
                max_depth (int): Maximum allowed depth for elements.
            """
            
            with ProcessPoolExecutor() as executor:
                futures = []
                for element in population:
                    if element.fitness == np.inf:
                        future = executor.submit(self.single_element_fitness, element, data, depth_penalty, max_depth)
                        futures.append(future)
                
                for future in futures:
                    future.result()
        

    def single_element_fitness(self, element, data, depth_penalty, max_depth):
        """
        Calculates the fitness value for a single element based on the given data.

        Args:
            element: The element for which the fitness value is calculated.
            data: The data used for evaluating the fitness value.
            depth_penalty: The penalty factor for exceeding the maximum depth.
            max_depth: The maximum allowed depth for the element.

        Returns:
            The fitness value calculated for the element.
        """
        fitness_value = 0
        for i in data:
            try:
                fitness_value += (i["result"] - element.evaluate(i["x"], i["y"]))**2
            except OverflowError:
                fitness_value = float('inf')
                break
        fitness_value = fitness_value/len(data)
        if element.compute_depth() <= max_depth:
            element.value = fitness_value
            element.fitness = fitness_value
            return
        element.value = fitness_value
        fitness_value += depth_penalty*element.depth
        element.fitness = fitness_value
        return fitness_value
   

