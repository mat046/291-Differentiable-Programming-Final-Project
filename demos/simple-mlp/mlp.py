def square(x : float) -> float:
    mulf(x, x)

def relu(x : float) -> float:
    ifelsef(greaterf(x, 0.0), x, 0.0)

def hidden_layer_helper(input : float, w_in : float, b_in : float) -> float:
    relu(addf(mulf(input, w_in), b_in))

# collects output from half of the neurons in an 8-neuron hidden layer
def output_layer_helper(
    w1 : float, t1 : float,
    w2 : float, t2 : float,
    w3 : float, t3 : float,
    w4 : float, t4 : float,
) -> float:
    addf(
        addf(
            mulf(w1, t1),
            mulf(w2, t2)
        ),
        addf(
            mulf(w3, t3),
            mulf(w4, t4)
        )
    )

# collects output from an 8-neuron hidden layer
def output_layer(
    w_out_1 : float, temp_in_1 : float,
    w_out_2 : float, temp_in_2 : float,
    w_out_3 : float, temp_in_3 : float,
    w_out_4 : float, temp_in_4 : float,
    w_out_5 : float, temp_in_5 : float,
    w_out_6 : float, temp_in_6 : float,
    w_out_7 : float, temp_in_7 : float,
    w_out_8 : float, temp_in_8 : float,
    b_out : float
) -> float:
    addf(
        addf(
            output_layer_helper(
                w_out_1, temp_in_1,
                w_out_2, temp_in_2,
                w_out_3, temp_in_3,
                w_out_4, temp_in_4
            ),
            output_layer_helper(
                w_out_5, temp_in_5,
                w_out_6, temp_in_6,
                w_out_7, temp_in_7,
                w_out_8, temp_in_8
            ),
        ),
        b_out
    )


def model(
    input : float,

    w_in_1 : float, w_in_2 : float, w_in_3 : float, w_in_4 : float,
    w_in_5 : float, w_in_6 : float, w_in_7 : float, w_in_8 : float,

    b_in_1 : float, b_in_2 : float, b_in_3 : float, b_in_4 : float,
    b_in_5 : float, b_in_6 : float, b_in_7 : float, b_in_8 : float,

    w_out_1 : float, w_out_2 : float, w_out_3 : float, w_out_4 : float,
    w_out_5 : float, w_out_6 : float, w_out_7 : float, w_out_8 : float,
    b_out : float
) -> float:
    output_layer(
        w_out_1, hidden_layer_helper(input, w_in_1, b_in_1),
        w_out_2, hidden_layer_helper(input, w_in_2, b_in_2),
        w_out_3, hidden_layer_helper(input, w_in_3, b_in_3),
        w_out_4, hidden_layer_helper(input, w_in_4, b_in_4),
        w_out_5, hidden_layer_helper(input, w_in_5, b_in_5),
        w_out_6, hidden_layer_helper(input, w_in_6, b_in_6),
        w_out_7, hidden_layer_helper(input, w_in_7, b_in_7),
        w_out_8, hidden_layer_helper(input, w_in_8, b_in_8),
        b_out
    )

def loss(
    # input layer
    input : float,


    # hidden layer
    w_in_1 : float, w_in_2 : float, w_in_3 : float, w_in_4 : float,
    w_in_5 : float, w_in_6 : float, w_in_7 : float, w_in_8 : float,

    b_in_1 : float, b_in_2 : float, b_in_3 : float, b_in_4 : float,
    b_in_5 : float, b_in_6 : float, b_in_7 : float, b_in_8 : float,


    # output layer
    w_out_1 : float, w_out_2 : float, w_out_3 : float, w_out_4 : float,
    w_out_5 : float, w_out_6 : float, w_out_7 : float, w_out_8 : float,
    b_out : float,


    # function to approximate
    target : float
) -> float:
    square(
        subf(
            model(
                input,

                w_in_1, w_in_2, w_in_3, w_in_4,
                w_in_5, w_in_6, w_in_7, w_in_8,

                b_in_1, b_in_2, b_in_3, b_in_4,
                b_in_5, b_in_6, b_in_7, b_in_8,

                w_out_1, w_out_2, w_out_3, w_out_4,
                w_out_5, w_out_6, w_out_7, w_out_8,

                b_out
            ),
            target
        )
    )

d_loss = rev_diff(loss)