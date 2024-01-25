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
        self.functions = ['+', '-', '*', '/', 'sqrt', 'sigmoid']
        self.fitness = np.inf
        self.value = np.inf

    def is_leaf(self):
        """
        Check if the node is a leaf node.

        Returns:
            bool: True if the node is a leaf, False otherwise.
        """
        if self.left is None and self.right is None:
            return True
    
    
    def full(self, initial_depth, depth=0, parent=None):
            """
            Generates a single individual with the specified initial depth using full method.

            Parameters:
            - initial_depth (int): The initial depth of the tree.
            - depth (int): The current depth of the node (default: 0).
            - parent (Tree): The parent node of the current node (default: None).
            """
            variables = ['x', 'y']

            if depth == initial_depth:
                if random.random() < 0.5:
                    self.data = random.choice(variables)
                else:
                    self.data = random.randint(1,9)
                
                self.parent = parent
                return
            
            self.data = random.choice(self.functions)
            self.parent = parent

            if self.data == 'sqrt' or self.data == 'sigmoid':
                self.left = Tree()
                self.left.full(initial_depth, depth+1, self)
                return
            else:
                self.left = Tree()
                self.left.full(initial_depth, depth+1, self)
                
                self.right = Tree()
                self.right.full(initial_depth, depth+1, self)
                return


    def grow(self, initial_depth, depth=0, parent=None):
            """
            Generates a single individual with the specified initial depth using grow method.

            Parameters:
            - initial_depth (int): The initial depth of the tree.
            - depth (int): The current depth of the tree (default: 0).
            - parent (Tree): The parent node of the current node (default: None).
            """
            # if depth is equal to initial depth, then the node is a leaf
            numbers = list(range(1, 10))

            # Create an array of strings
            variables = ['x', 'y']

            terminals = numbers+ variables

            if depth == initial_depth:
                #for leaf nodes, randomly choose a value or variable
                if random.random() < 0.5:
                    #adds a variable to the leaf node
                    self.data = random.choice(variables)
                else:
                    #adds a value to the leaf node
                    self.data = random.randint(1,9)
                
                self.parent = parent
                return

            choice_set = self.functions + terminals
            self.data = random.choice(choice_set)
            self.parent = parent

            if self.data in terminals:
                return

            # if function is sqrt or sigmoid, then it is a unary function so only generates lef tree
            if self.data == 'sqrt' or self.data == 'sigmoid':
                self.left = Tree()
                self.left.grow(initial_depth, depth+1, self)
                return
            # if function is not sqrt or sigmoid, then it is a binary function so generates left and right trees
            else:
                self.left = Tree()
                self.left.grow(initial_depth, depth+1, self)
                
                self.right = Tree()
                self.right.grow(initial_depth, depth+1, self)
                return

    
    def ramped_half_and_half(self, max_depth):
        """
        Randomly chooses between the grow and full methods to create a tree.

        Parameters:
        - max_depth (int): The maximum depth of the tree.

        Returns:
        None
        """
        if random.random() < 0.5:
            self.grow(max_depth)
        else:
            self.full(max_depth)


    def evaluate(self, x, y):
        """
        Evaluates the expression tree rooted at this node given the x y values from a given dataset.

        Args:
            x (float): The value of variable x.
            y (float): The value of variable y.

        Returns:
            float: The result of evaluating the expression tree.

        Raises:
            ValueError: If an invalid operation or function is encountered.
            OverflowError: If an overflow occurs during the computation.
        """
        if self.is_leaf():
            if self.data == 'x':
                return x
            elif self.data == 'y':
                return y
            else:
                return self.data
        if self.data == '+':
            return self.left.evaluate(x, y) + self.right.evaluate(x, y)
        if self.data == '-':
            return self.left.evaluate(x, y) - self.right.evaluate(x, y)
        if self.data == '*':
            return self.left.evaluate(x, y) * self.right.evaluate(x, y)
        if self.data == '/':
            return self.left.evaluate(x, y) / (self.right.evaluate(x, y) + 1e-10)
        if self.data == 'sqrt':
            try:
                return math.sqrt(self.left.evaluate(x, y))
            except ValueError:
                return 1

        if self.data == 'sigmoid':
            try:
                return 1.0 / (1.0 + np.exp(-np.clip(self.left.evaluate(x, y), -709, 709)))
            except OverflowError:
                return 1


    def compute_depth(self):
        """
        Computes the depth of the tree

        Returns:
            int: The depth of the current node.
        """
        if self.is_leaf():
            return 0
        else:
            left_depth = self.left.compute_depth() if self.left else 0
            right_depth = self.right.compute_depth() if self.right else 0
            self.depth = max(left_depth, right_depth) + 1
            return self.depth

    
    def random_subtree(self, stop_p = 0):
            """
            Searches a ranndom subtree and returns it.(for variation operators)

            Parameters:
            - stop_p (float): The stopping probability for expanding the subtree. Default is 0.

            Returns:
            - Node: The randomly selected subtree.
            """
            # Randomly choose left or right subtree
            if random.random() > stop_p:
                # increments stopping chance with random number
                stop_p += random.random()
                
                # expands left tree with 50% chance otherwise expands right subtree
                if random.random() < 0.5:
                    if self.left:
                        return self.left.random_subtree(stop_p)
                    else:
                        return self
                else:
                    if self.right:
                        return self.right.random_subtree(stop_p)
                    elif self.left:
                        return self.left.random_subtree(stop_p)
                    else:
                        return self
            else:
                return self
    
    
    def swap_subtree(self, old, new):
            """
            Swaps a subtree in the tree with a new subtree.

            Args:
                old: The subtree to be replaced.
                new: The new subtree to replace the old subtree.

            Returns:
                The modified tree with the subtree swapped.

            """
            if self == old:
                return copy.deepcopy(new)
            else:
                if self.left:
                    self.left = self.left.swap_subtree(old, new)
                if self.right:
                    self.right = self.right.swap_subtree(old, new)
                return self


    def __str__(self) -> str:
        """
        Returns a string representation of the tree.

        If the tree is a leaf node, it returns the string representation of the data.
        If the data is 'sqrt' or 'sigmoid', it returns the string representation of the data
        followed by the string representation of the left subtree enclosed in parentheses.
        Otherwise, it returns the string representation of the data followed by the string
        representation of the left and right subtrees enclosed in parentheses and separated by a comma.

        Returns:
            str: The string representation of the tree.
        """
        if self.is_leaf():
            return str(self.data)
        if self.data == 'sqrt' or self.data == 'sigmoid':
            return str(self.data) + '(' + str(self.left) + ')'
        return str(self.data) + '(' + str(self.left) + ',' + str(self.right) + ')'
    

    def __deepcopy__(self, memo):
        """
        Create a deep copy of the Tree object.

        Parameters:
            memo (dict): A dictionary that maps objects to their deep copies.

        Returns:
            Tree: A new instance of the Tree class with copied attributes.
        """

        # Create a new instance of the class.
        new_tree = Tree()

        # Copy the data manually.
        new_tree.data = self.data
        new_tree.depth = self.depth
        new_tree.functions = self.functions.copy()
        new_tree.fitness = self.fitness

        # Deep copy the left and right subtrees.
        if self.left is not None:
            new_tree.left = copy.deepcopy(self.left, memo)
        if self.right is not None:
            new_tree.right = copy.deepcopy(self.right, memo)

        # Don't deep copy the parent, as this would create a circular reference.
        new_tree.parent = self.parent

        return new_tree