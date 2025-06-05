def plussquare(x : float, y : float) -> float:
    mulf(addf(x, y), addf(x, y))


def poly(x : float, y : float, z : float) -> float:
    addf(plussquare(x, y), plussquare(y, z))

d_poly = rev_diff(poly)