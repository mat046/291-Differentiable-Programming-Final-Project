def quartic(x : float) -> float:
    mulf(mulf(x, x), mulf(x, x))

def quadruple(x : float) -> float:
    addf(addf(x, x), addf(x, x))

def func(x : float) -> float:
    quadruple(quartic(x))

d_func = rev_diff(func)