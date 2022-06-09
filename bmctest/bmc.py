# action move
# grid world
# goal: move to (3,3)

from z3 import *

solver = Solver()
Sq = DeclareSort("Square")

squares = [Sq("sq%d%d") for i in range(3) for j in range(3)]

print(squares)

def make_adj(dim=3):
    cons = []
    for i in range(dim):
        for j in range(dim):
for x, y in [(i-1,j), (i+1,j), (i, j-1), (i, j+1)]:
                if x < dim and x >= 0 and  y < dim and y >= 0:
                    cons += ["adj(b%d%d, b%d%d)" % (i, j, x, y)]
    return cons

#print(make_adj())

init = ["adj(%s,%s)"]
