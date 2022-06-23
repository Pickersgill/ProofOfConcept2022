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

StateSort, states = EnumSort("State", [n for n in at.preds])
ActionSort, [up, down, left, right] = EnumSort("Action", ["up", "down", "left", "right"])
T = Function("T", StateSort, StateSort, ActionSort, BoolSort())

s = Solver()

grid = [states[k:k+5] for k in range(0, len(states),5)]

for x1 in range(D):
    for y1 in range(D):
        sq1 = grid[y1][x1]
        for x2 in range(D):
            for y2 in range(D):
                sq2 = grid[y2][x2]
                unblocked = [x2, y2] not in obs
                # Left
                if x1 == x2 + 1 and y1 == y2 and unblocked:
                    s.add(T(sq1, sq2, left) == True)
                else:
                    s.add(T(sq1, sq2, left) == False)
                # Right
                if x1 == x2 - 1 and y1 == y2 and unblocked:
                    s.add(T(sq1, sq2, right) == True)
                else:
                    s.add(T(sq1, sq2, right) == False)
                # Up
                if x1 == x2  and y1 == y2 - 1 and unblocked:
                    s.add(T(sq1, sq2, down) == True)
                else:
                    s.add(T(sq1, sq2, down) == False)
                # Down
                if x1 == x2  and y1 == y2 + 1 and unblocked:
                    s.add(T(sq1, sq2, up) == True)
                else:
                    s.add(T(sq1, sq2, up) == False)

def search(depth):
    plan_states = [None for _ in range(depth)]
    plan_acts = [None for _ in range(depth)]

    for i in range(depth):
        plan_states[i] = Const("p%d" % i, StateSort)
        plan_acts[i] = Const("a%d" % i, ActionSort)

    init = grid[0][0]
    s.add(plan_states[0] == init)

    for i in range(depth-1):
        s.add(T(plan_states[i], plan_states[i+1], plan_acts[i]) == True)

    goal = grid[3][1]
    s.add(plan_states[-1] == goal)

    if s.check() == sat:
        return [s.model()[a] for a in plan_acts]
    else:
        return False

for l in range(1, 10):
    s.push()
    r = search(l)
    s.pop()
    if r:
        print(r)
        gif_builder.build(r, "plans/plan%d.gif" % l, D, [0,0], obs) 






