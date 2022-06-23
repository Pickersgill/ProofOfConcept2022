from z3 import  *
import numpy as np
import itertools

class IncorrectArityException(Exception):
    pass

class IncorrectArgTypeException(Exception):
    pass

class TimeOutOfBoundsException(Exception):
    pass

def to_pred_name(name, args):
    s = name + "_"
    s += "_".join([a for a in args])
    return s

class GroundPred:
    def __init__(self, name, args):
        self.name = to_pred_name(name, args)
        self.raw_name = name
        self.args = args

    def pred(self):
        return Bool(self.name)

    def __str__(self):
        return self.name


class Pred:
    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.arity = len(args)
        self.preds = {}
        self.flatten()
        
    def flatten(self):
        for comb in itertools.product(*[a.domain for a in self.args]):
            asStr = to_pred_name(self.name, comb)
            self.preds[asStr] = GroundPred(self.name, comb)

    def get_all(self):
        return self.preds.values()

    def __call__(self, *args):
        if len(args) != self.arity + 1:
            err = "'%s' accessed with incorrect arity (%d). " % (self.name, len(args)-1)
            err += "Expected arity %d" % (self.arity + 1)
            raise IncorrectArityException(err)
        elif any([a not in self.args[i].domain for i, a in enumerate(args[:-1])]):
            err = "Bad argument type or type ordering. "
            err += "Expected: " + self.name
            err += "(%s)" % (",".join([a.name for a in self.args + ["t"]]))
            raise IncorrectArgTypeException(err)
        else:
            return self.preds[to_pred_name(self.name, args[:-1])]
            
    def __str__(self):
        s = "Predicate{%s(%s)}" % (self.name, ",".join([str(t) for t in self.args]))
        return s
