def kuratowski_decomposition_string(array):
    assert isinstance(array, list) or isinstance(array, tuple), "function argument must be of type list or tuple"
    array = list(array)
    n = len(array)
    for i in range(n):
        if isinstance(array[i], list) or isinstance(array[i], tuple):
            array[i] = kuratowski_decomposition_string(array[i])
        else:
            pass
    if n == 1:
        x = array[0]
        l = "{"
        r = "}"
        return f"{l}{l}{x}{r}{r}"
    elif n == 2:
        x = array[0]
        y = array[-1]
        l = "{"
        r = "}"
        s = f"{l}{l}{x}{r}, {l}{x}, {y}{r}{r}"
        return s
    else:
        v = array[:-1]
        y = array[-1]
        return kuratowski_decomposition_string([kuratowski_decomposition_string(v), y])