import random
import math
import numpy as np
import copy


# definition of the Inndividual class and its methods
class Tree:

    def __init__(self):
        self.data = None
        self.right = None
        self.left = None
        self.parent = None
        self.depth = 0
        self.operation = ['+', '-', '*', '/', 'sqrt', 'sigmoid']

    def is_leaf(self):
        if self.left is None and self.right is None:
            return True
    
    def generate(self, initial_depth, depth=0, parent=None):
        # if depth is equal to initial depth, then the node is a leaf
        self.depth = initial_depth

        if depth == initial_depth:
            #for leaf nodes, randomly choose a value
            self.data = random.randint(10,100)
            
            self.parent = parent
            return
        
        # for internal nodes, randomly choose an operation
        self.data = random.choice(self.operation)
        self.parent = parent

        # if operation is sqrt or sigmoid, then it is a unary operation so only generates lef tree
        if self.data == 'sqrt' or self.data == 'sigmoid':
            self.left = Tree()
            self.left.generate(initial_depth, depth+1, self)
            return
        # if operation is not sqrt or sigmoid, then it is a binary operation so generates left and right trees
        else:
            self.left = Tree()
            self.left.generate(initial_depth, depth+1, self)
            
            self.right = Tree()
            self.right.generate(initial_depth, depth+1, self)
            return

    # evaluates the value of the tree
    def evaluate(self):
        if self.is_leaf():
            return self.data
        if self.data == '+':
            return self.left.evaluate() + self.right.evaluate()
        if self.data == '-':
            return self.left.evaluate() - self.right.evaluate()
        if self.data == '*':
            return self.left.evaluate() * self.right.evaluate()
        if self.data == '/':
            try:
                return self.left.evaluate() / self.right.evaluate()
            except ZeroDivisionError:
                return np.inf
        if self.data == 'sqrt':
            try:
                return math.sqrt(self.left.evaluate())
            except ValueError:
                return np.inf
            
        if self.data == 'sigmoid':
            return 1.0 / (1.0 + np.exp(-self.left.evaluate()))



    def compute_depth(self):
        if self.is_leaf():
            return 0
        else:
            left_depth = self.left.compute_depth() if self.left else 0
            right_depth = self.right.compute_depth() if self.right else 0
            return max(left_depth, right_depth) + 1


    def random_subtree(self, stop_p = 0):
        # Randomly choose left or right subtree
        if random.random() > stop_p:
            # increments stopping chance with random number
            stop_p = stop_p = random.random()
            
            # expands left tree with 50% chance otherwise expands right subtree
            if random.random() < 0.5:
                if self.left:
                    return self.left.random_subtree(stop_p)
                else:
                    return self
            else:
                if self.right:
                    return self.right.random_subtree(stop_p)
                else:
                    return self
        else:
            return self
        
    def swap_subtree(self, old, new):
        if self == old:
            return copy.deepcopy(new)
        else:
            if self.left:
                self.left = self.left.swap_subtree(old, new)
            if self.right:
                self.right = self.right.swap_subtree(old, new)
            return self



    def __str__(self) -> str:
        if self.is_leaf():
            return str(self.data)
        if self.data == 'sqrt' or self.data == 'sigmoid':
            return str(self.data) + '(' + str(self.left) + ')'
        return str(self.data) + '(' + str(self.left) + ',' + str(self.right) + ')'