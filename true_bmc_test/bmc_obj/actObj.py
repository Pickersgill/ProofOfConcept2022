from z3 import  *
import numpy as np

from .predObj import Pred, IncorrectArgTypeException, IncorrectArityException

class Act:
    # args must be dictionary form
    def __init__(self, name, args, t):
        self.name = name
        self.arg_types = list(args.values())
        self.arg_names = list(args.keys())
        self.pred_name = name + "_" + "_".join(self.arg_names)
        self.args = [Pred(name + "_" + _name, [_type], t) for (_name, _type) in args.items()]
        self.t = t
        self.arity = len(self.args)
        
    def pred(self, t):
        return Bool(self.pred_name + str(t))

    def get_pre(self, args, t):
        print("USING DEFAULT PRECONDTION FOR %s" % self.pred_name)
        return True

    def get_add(self, args, t):
        print("USING DEFAULT ADD FOR %s" % self.pred_name)
        return []

    def get_del(self, args, t):
        print("USING DEFAULT DEL FOR %s" % self.pred_name)
        return []

    def __call__(self, *cargs):
        if len(cargs) != self.arity + 1:
            err = "'%s' accessed with incorrect arity (%d). " % (self.name, len(cargs) - 1)
            err += "Expected arity %d" % self.arity
            raise IncorrectArityException(err)
        elif any([cargs[i] not in self.arg_types[i].domain for i in range(self.arity)]):
            err = "Bad argument type or type ordering. "
            err += "Expected: " + self.name
            err += "(%s)" % (",".join([a.name for a in self.arg_types]))
            raise IncorrectArgTypeException(err)
        else:
            return [arg(cargs[i], cargs[-1]) for i, arg in enumerate(self.args)]
            
    def __str__(self):
        s = "Action{%s(%s)}" % (self.name, ",".join([str(t) for t in self.arg_types]))
        return s
