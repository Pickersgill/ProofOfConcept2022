try:
    from . import predObj
    from . import actObj
    from . import typeObj
except:
    import predObj
    import actObj
    import typeObj

Pred = predObj.Pred
Act = actObj.Act
Type = typeObj.Type
