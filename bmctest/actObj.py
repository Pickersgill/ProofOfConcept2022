from z3 import  *
import numpy as np
import itertools

class GroundAct:
    def __init__(self, name, args, t):
        self.name = name + str(t)
        self.args = args
        self.t = t

    def __str__(self):
        s = "Action '%s(%s)'" % (self.name, ",".join(self.args))
        return s

class Act:
    def __init__(self, name, args, t):
        self.name = name
        self.args = args
        self.t = t
        self.arity = len(args)
        self.ground_acts = {}
        self.flatten()
        
    def to_pred_name(self, args, t):
        s = self.name + "_"
        s += "_".join([a for a in args])
        return s
        
    def flatten(self):
        print("flattening '%s'" % self.name)
        
        for comb in itertools.product(*[a.domain for a in self.args]):
            asStr = self.to_pred_name(comb)
            self.ground_acts[asStr] = GroundAct(self.name, comb)

    def __call__(self, *args):
        if len(args) != self.arity:
            err = "'%s' accessed with incorrect arity (%d). " % (self.name, len(args))
            err += "Expected arity %d" % self.arity
            raise IncorrectArityException(err)
        elif any([a not in self.args[i].domain for i, a in enumerate(args)]):
            err = "Bad argument type or type ordering. "
            err += "Expected: " + self.name
            err += "(%s)" % (",".join([a.name for a in self.args]))
            raise IncorrectArgTypeException(err)
        else:
            return self.ground_acts[self.to_pred_name(args)]
            
