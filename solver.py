from z3 import *

class SudokuSolver:
    def __init__(self):
        print("Spawned a new solver...")
        
    def solve(self, problem):
        s = Solver()

        ints = [[Int("cell%s%s" % (i, j)) for i in range(9)] for j in range(9)]

        num_constraints = [And(1 <= ints[i][j], ints[i][j] <= 9)
                           for i in range(9) for j in range(9)]
        
        row_constraints = [Distinct(ints[i]) for i in range(9)]
        col_constraints = [Distinct([ints[i][j] for j in range(9)]) for i in range(9)]

        box_constraints = [Distinct([ints[i][j]
                                    for i in range(x,x+3) for j in range(y,y+3)]
                                    ) for x in range(0,9,3) for y in range(0, 9, 3)
                                    ]
        
        eq_constraints = [If(problem[i][j] == 0,
                             True,
                             ints[i][j] == problem[i][j])
                             for i in range(9) for j in range(9)]
        
        constraints = row_constraints
        constraints += col_constraints
        constraints += box_constraints
        constraints += eq_constraints
        constraints += num_constraints

        s.add(constraints)
        s.check()

        if s.check() == sat:
            model = s.model()
            solution = [[model.evaluate(ints[j][i]).as_long() for i in range(9)]for j in range(9)]
            return solution
        else:
            return False
        
        
                        
        

        
