from z3 import  *
import numpy as np
import itertools

class IncorrectArityException(Exception):
    pass

class IncorrectArgTypeException(Exception):
    pass

def to_pred_name(name, args, t):
    s = name + "_"
    s += "_".join([a for a in args])
    s += "_" + str(t)
    return s

class GroundPred:
    def __init__(self, name, args, t):
        self.name = to_pred_name(name, args, t)
        self.raw_name = name
        self.args = args
        self.t = t

    def pred(self):
        return Bool(self.name)

    def pred_at_time(self, t):
        return Bool(to_pred_name(self.raw_name, self.args, t))

    def __str__(self):
        return self.name


class Pred:
    def __init__(self, name, args, t):
        self.name = name
        self.args = args
        self.arity = len(args)
        self.preds = {}
        self.t = t
        self.flatten()
        
    def flatten(self):
        print("flattening '%s'" % self.name)
        
        for t in range(self.t + 1):
            for comb in itertools.product(*[a.domain for a in self.args]):
                asStr = to_pred_name(self.name, comb, t)
                self.preds[asStr] = GroundPred(self.name, comb, t)

    def get_all(self):
        return self.preds.values()

    def __call__(self, *args):
        if len(args) != self.arity + 1:
            err = "'%s' accessed with incorrect arity (%d). " % (self.name, len(args))
            err += "Expected arity %d" % (self.arity + 1)
            raise IncorrectArityException(err)
        elif any([a not in self.args[i].domain for i, a in enumerate(args[:-1])]):
            err = "Bad argument type or type ordering. "
            err += "Expected: " + self.name
            err += "(%s)" % (",".join([a.name for a in self.args + ["t"]]))
            raise IncorrectArgTypeException(err)
        else:
            return self.preds[to_pred_name(self.name, args[:-1], args[-1])]
            
