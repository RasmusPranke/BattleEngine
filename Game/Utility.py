def sum(to):
    return (to * (to + 1)) / 2

def sumsum(to):
    return (to * (to + 1) * (2 * to + 4)) / 12

def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el