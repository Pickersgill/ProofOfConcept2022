from z3 import *
from bmc_obj import Pred, Type
import gif_builder

"""
Grid navigation problem:
    - 1 fluid "at", position of agent
    - 1 constant "adj", defines adjacency of squares
"""

D = 5

loc = Type("loc")

for i in range(D):
    for j in range(D):
        loc.add("sq%d%d" % (i, j))

at = Pred("at", [loc])
at.flatten()

adj = Pred("adj", [loc, loc])
obs = [[0,1], [1,1], [2,1], [3,3]]

StateSort, states = EnumSort("State", [n for n in at.preds] + ["sink"])
ActionSort, [up, down, left, right] = EnumSort("Action", ["up", "down", "left", "right"])
T = Function("T", StateSort, ActionSort, StateSort)

s = Solver()

grid = [states[k:k+5] for k in range(0, len(states)-1,5)]
for g in grid:
    print(g)

sink = states[-1]

s.add([T(sink, a) == sink for a in [up, down, left, right]])

for x1 in range(D):
    for y1 in range(D):
        sq1 = grid[y1][x1]

        # LEFT
        if x1 - 1 >= 0 and [x1-1, y1] not in obs:
            s.add(T(sq1, left) == grid[y1][x1-1])
        else:
            s.add(T(sq1, left) == sink)
        # RIGHT
        if x1 + 1 < D and [x1+1, y1] not in obs:
            s.add(T(sq1, right) == grid[y1][x1+1])
        else:
            s.add(T(sq1, right) == sink)
        # UP
        if y1 - 1 >= 0 and [x1, y1-1] not in obs:
            s.add(T(sq1, up) == grid[y1-1][x1])
        else:
            s.add(T(sq1, up) == sink)
        # DOWN
        if y1 + 1 < D and [x1, y1+1] not in obs:
            s.add(T(sq1, down) == grid[y1+1][x1])
        else:
            s.add(T(sq1, down) == sink)

def search(depth):
    plan_states = [None for _ in range(depth)]
    plan_acts = [None for _ in range(depth)]

    for i in range(depth):
        plan_states[i] = Const("s%d" % i, StateSort)
        plan_acts[i] = Const("a%d" % i, ActionSort)

    init = grid[0][0]
    s.add(plan_states[0] == init)

    for i in range(depth-1):
        s.add(plan_states[i] != sink)
        s.add(T(plan_states[i], plan_acts[i]) == plan_states[i+1])

    goal = grid[0][2]
    s.add(plan_states[-1] == goal)

    if s.check() == sat:
        return [s.model()[a] for a in plan_acts]
    else:
        return False

for l in range(1,10):
    s.push()
    r = search(l)
    #print(s)
    s.pop()
    if r:
        print(r)
        gif_builder.build(r, "plans/plan%d.gif" % l, D, [0,0], obs) 
    else:
        print("Failed to solve within k=%d" % l)



