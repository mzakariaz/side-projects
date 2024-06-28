def kuratowski_decomposition_set(array):
    assert isinstance(array, list) or isinstance(array, tuple), "function argument must be of type list or tuple"
    array = list(array)
    n = len(array)
    for i in range(n):
        if isinstance(array[i], list) or isinstance(array[i], tuple):
            array[i] = kuratowski_decomposition_set(array[i])
        else:
            pass
    if n == 1:
        x = array[0]
        return frozenset([frozenset([x])])
    elif n == 2:
        x = array[0]
        y = array[1]
        return frozenset([frozenset([x]), frozenset([x, y])])
    else:
        v = array[:-1]
        y = array[-1]
        return kuratowski_decomposition_set([kuratowski_decomposition_set(v), y])