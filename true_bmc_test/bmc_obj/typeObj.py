from z3 import  *
import numpy as np
import itertools

class Type:
    def __init__(self, name):
        self.name = name
        self.domain = []

    def add(self, name):
        self.domain += [name]

    def size(self):
        return len(self.domain)
        
    def __str__(self):
        return "Type{%s}" % self.name
