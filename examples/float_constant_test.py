def func(x : float) -> float:
    addf(mulf(x, 2.0), divf(x, 2.0))

d_func = rev_diff(func)