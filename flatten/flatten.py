def flatten(l):
    if len(l) == 0:
        return []
    if len(l) == 1:
        if isinstance(l[0], list):
            return flatten(l[0])
        return l
    return flatten(l[0:1]) + flatten(l[1:])
