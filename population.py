from math import nan
import random
from tree import Tree
import numpy as np
from time import sleep
import copy
import math




class Population:

    def __init__(self, population_size, min_depth ,max_depth):
        self.population_size = population_size
        self.max_depth = max_depth
        self.min_depth = min_depth
        self.population = []
        self.parents = []
        self.offspring = []
        
    # initializes the population
    def initialize(self):
        for i in range(self.population_size):
            t = Tree()
            t.generate(random.randint(self.min_depth, self.max_depth))
            self.population.append(t)
        #for element in self.population:
            #print(element.evaluate())
    
    # TODO: implement the passage of generations


    def select_pool(self, k):
        # selects a mating pool of size k(better if even) 
        # in a tournament fashion
        pop_copy = copy.deepcopy(self.population)
        mating_pool = []
        for i in range(k):
            if len(pop_copy) < 2:
                break
            s1,s2 = np.random.choice(pop_copy, size=2, replace=False)
            pop_copy.remove(s1)
            pop_copy.remove(s2)
            if abs(s1.evaluate()) >= abs(s2.evaluate()):
                mating_pool.append(s1)
            else:
                mating_pool.append(s2)

        return mating_pool


    # Function that given 2 elements performs crossover
    def crossover(self, p1, p2, max_depth):
        # select a random subtree of p1 and p2
        s1 = p1.random_subtree()
        s2 = p2.random_subtree()
      
        

        p1 = p1.swap_subtree(s1, s2)
        p2 = p2.swap_subtree(s2, s1)
    
        if p1.compute_depth() > max_depth or p2.compute_depth()>max_depth:
            #print("Tree is Bloating, discarding offspring...")
            return
        self.population.append(p1)
        self.population.append(p2)

    # Function that applyes mutation to p
    def mutation(self, p, max_depth):
        #print(f'p before mutation: {p}')
        s = p.random_subtree()
        m = Tree()
        m.generate(random.randint(2, 3))
        #print(f'mutation m : {m}')
        p = p.swap_subtree(s,m)
        if p.compute_depth() > max_depth:
            return
        #print(f'p after mutation: {p}')
        self.population.append(p)

    
    def calculate_fitness(self, result):
        fitness = []
        for element in self.population:
            if math.isnan(element.evaluate()):
                fitness_value = np.inf
            else:
                fitness_value = abs(element.evaluate() - result)
            fitness.append(fitness_value)
            evaluated = zip(self.population, fitness)
        return evaluated
    
    # best method
    def best(self):
        # returns the best element of the population
        return self.population[0].evaluate()

    # size of the population
    def size(self):
        return len(self.population)
    
    
    '''
    # crossover method
    def crossover(self, p1,p2):
        # selects a random subtree from each parent and switches them
        target1 = random.randint(1, p1.depth)   
        target2 = random.randint(1, p2.depth)

        r1 = p1.crossover_select(target1)
        r2 = p2.crossover_select(target2)

        # switch subtrees
        p1.replace_child(r1, r2, p1.depth)
        p2.replace_child(r2, r1, p2.depth)

        p1.depth = p1.depth - target1 + target2
        p2.depth = p2.depth - target2 + target1

        print(f'crossover {r1} and {r2}')

        # add elements to the population
        self.population.append(p1)
        self.population.append(p2)
    
    # mutation method
    def mutation(self, mating_pool):
        # selects a random element from the mating pool and mutates it
        element = random.choice(mating_pool)
        # get random subtree from element
        target = random.randint(1, element.depth)
        r1 = element.crossover_select(target)
        # generate new subtree
        r2 = Tree()
        r2.generate(random.randint(2, self.max_depth))
        # replace subtree
        element.replace_child(r1, r2, element.depth)
        element.depth = element.depth - target + r2.depth
        self.population.append(element)
        #print(f'crossover {r}')
    '''

    