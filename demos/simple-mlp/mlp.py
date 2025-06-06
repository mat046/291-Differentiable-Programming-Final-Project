def square(x : float) -> float:
    mulf(x, x)

def relu(x : float) -> float:
    ifelsef(greaterf(x, 0.0), x, 0.0)

def hidden_layer_helper(input : float, w_in : float, b_in : float) -> float:
    relu(addf(mulf(input, w_in), b_in))

def output_layer_helper(
    w_out_1 : float, temp_in_1 : float,
    w_out_2 : float, temp_in_2 : float,
    w_out_3 : float, temp_in_3 : float,
    w_out_4 : float, temp_in_4 : float,
    b_out : float
) -> float:
    addf(
        addf(
            addf(
                mulf(w_out_1, temp_in_1),
                mulf(w_out_2, temp_in_2)
            ),
            addf(
                mulf(w_out_3, temp_in_3),
                mulf(w_out_4, temp_in_4)
            )
        ),
        b_out
    )


def mlp(
    # input layer
    input : float,

    # hidden layer
    w_in_1 : float, w_in_2 : float, w_in_3 : float, w_in_4 : float,
    b_in_1 : float, b_in_2 : float, b_in_3 : float, b_in_4 : float,

    # output layer
    w_out_1 : float, w_out_2 : float, w_out_3 : float, w_out_4 : float,
    b_out : float,

    # function to approximate
    target : float,
) -> float:
    square(
        subf(
            output_layer_helper(
                w_out_1, hidden_layer_helper(input, w_in_1, b_in_1),
                w_out_2, hidden_layer_helper(input, w_in_2, b_in_2),
                w_out_3, hidden_layer_helper(input, w_in_3, b_in_3),
                w_out_4, hidden_layer_helper(input, w_in_4, b_in_4),
                b_out
            ),
            target
        )
    )

d_mlp = rev_diff(mlp)