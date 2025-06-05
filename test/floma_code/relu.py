
def relu(x : float) -> float:
    ifelsef(greaterf(x, 0.0), x, 0.0)

d_relu = rev_diff(relu)