
def func(x : float, y : float) -> float:
    add(mul(x, y), div(x, y))

d_func = rev_diff(func)