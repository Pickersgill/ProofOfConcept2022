from z3 import  *
import numpy as np
import itertools
from typeObj import Type
from actObj import Act
from predObj import Pred

"""
The Monkey and Banana Problem (AIMA 10.4):

- The monkey wants the banana
- The banana is hanging from the roof (out of reach) HIGH
- The monkey is LOW, he cannot reach the banana
- There is a box on the ground, the box is also LOW
- The monkey is at A
- The banana is at B
- The box is at C
- The monkey has actions:
    + Go (move from one place to another
    + Push (push object from one place to another)
    + ClimbUp (climb onto)
    + ClimbDown (climb down from)
    + Grasp/Ungrasp (grasp object that is the same place and height as monkey) 

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Eyes much bigger than my stomach here.

Turns out implementing this (theoretically easy) example is actually very hard.
Instead I've tried a REALLY simple example where the only action is "go" and there are
just two positions (A and B).
"""
    
loc = Type("loc")
[loc.add(s) for s in "AB"]
T = 1

at = Pred("at", [loc], T)
go = Pred("go", [loc, loc], T)

def get_go_pre(go_act):
    pre = [at(go_act.args[0], go_act.t)]
    return pre

def get_go_add(go_act):
    add = [at(go_act.args[1], go_act.t + 1)]
    return add

def get_go_rem(go_act):
    rem = [at(go_act.args[0], go_act.t + 1)]
    return rem

def get_initial():
    ini = And(
        at("A", 0).pred(),
        Not(at("B", 0).pred())
        )
    return ini

def get_goal():
    goal = And(
        at("B", T).pred()
        )
    return goal

def get_successor_axioms(preds, acts):
    clauses = []
    for pred in preds:
        cause_F = []
        cause_not_F = []

        for act in acts:
            if act.t < T:
                if pred in get_go_add(act):
                    cause_F += [act.pred()]
                elif pred in get_go_rem(act):
                    cause_not_F += [act.pred()]

        if len(cause_F) > 0 or len(cause_not_F) > 0:
            cause = Or(cause_F)
            not_cause = And(pred.pred(), Or(cause_not_F))
            clauses += [(pred.pred() == Or(cause, not_cause))]

    return And(clauses)

def get_precon_axioms(acts):
    clauses = []

    for act in acts:
        clauses += [Implies(act.pred(), And([p.pred() for p in get_go_pre(act)]))]

    return And(clauses)

def get_exclusion_axioms(acts):
    clauses = []
    for act1 in acts:
        for act2 in acts:
            if act1 != act2 and act1.t == act2.t:
                clauses += [Or(Not(act1.pred()), Not(act2.pred()))]

    return And(clauses)

ini = get_initial()
goal = get_goal()

acts = go.get_all()
preds = at.get_all()
succs = get_successor_axioms(preds, acts)
precon = get_precon_axioms(acts)
exclusion = get_exclusion_axioms(acts)

full = And(ini, goal, succs, precon, exclusion)
print(full)

solver = Solver()
solver.add(full)

print(solver.check())
if solver.check() == sat:
    m = solver.model()
    plan = []
    for t in range(T):
        for act in acts:
            if act.t == t and m.evaluate(act.pred()):
                plan += [act.name]
    print("Satisfied model...")
    print(m)
    print("\nExtracted plan: ")
    print(plan)


