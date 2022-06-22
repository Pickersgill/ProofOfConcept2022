from z3 import *

StateSort, states = EnumSort("State", ["s1", "s2"])
ActionSort, acts = EnumSort("Action", ["a1", "a2"])

T = Function("T", StateSort, StateSort, ActionSort, BoolSort())

s1, s2 = states
a1, a2 = acts

q1, q2 = Consts("q1 q2", StateSort)
q3 = Const("q3", ActionSort)

s = Solver()
s.add(T(s1, s2, a1) == True)
s.add(T(s1, s2, a2) == False)
s.add(T(q1, q2, q3) == True)

print(s.check())
m = s.model()
print(m)
