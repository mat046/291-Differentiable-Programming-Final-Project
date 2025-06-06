def mypow(x : float, n : int) -> float:
    ifelsef(
        greateri(n, 1),
        mulf(x, mypow(x, subi(n, 1))),
        x
    )

d_mypow = rev_diff(mypow)