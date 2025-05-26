
def func(x : float, y : float) -> float:
    addf(mulf(x, y), divf(x, y))

d_func = rev_diff(func)