import mlp
import numpy as np
import matplotlib.pyplot as plt


# function to approximate
def target_func(x):
    return -x**2
input_lower_bound = -5
input_upper_bound = 5

def train():
    num_training_steps = 10000

    # hidden layer
    w_in_1 = mlp.make__dfloat(np.random.normal(), 0.0)
    w_in_2 = mlp.make__dfloat(np.random.normal(), 0.0)
    w_in_3 = mlp.make__dfloat(np.random.normal(), 0.0)
    w_in_4 = mlp.make__dfloat(np.random.normal(), 0.0)
    w_in_5 = mlp.make__dfloat(np.random.normal(), 0.0)
    w_in_6 = mlp.make__dfloat(np.random.normal(), 0.0)
    w_in_7 = mlp.make__dfloat(np.random.normal(), 0.0)
    w_in_8 = mlp.make__dfloat(np.random.normal(), 0.0)

    b_in_1 = mlp.make__dfloat(np.random.normal(), 0.0)
    b_in_2 = mlp.make__dfloat(np.random.normal(), 0.0)
    b_in_3 = mlp.make__dfloat(np.random.normal(), 0.0)
    b_in_4 = mlp.make__dfloat(np.random.normal(), 0.0)
    b_in_5 = mlp.make__dfloat(np.random.normal(), 0.0)
    b_in_6 = mlp.make__dfloat(np.random.normal(), 0.0)
    b_in_7 = mlp.make__dfloat(np.random.normal(), 0.0)
    b_in_8 = mlp.make__dfloat(np.random.normal(), 0.0)

    # output layer
    w_out_1 = mlp.make__dfloat(np.random.normal(), 0.0)
    w_out_2 = mlp.make__dfloat(np.random.normal(), 0.0)
    w_out_3 = mlp.make__dfloat(np.random.normal(), 0.0)
    w_out_4 = mlp.make__dfloat(np.random.normal(), 0.0)
    w_out_5 = mlp.make__dfloat(np.random.normal(), 0.0)
    w_out_6 = mlp.make__dfloat(np.random.normal(), 0.0)
    w_out_7 = mlp.make__dfloat(np.random.normal(), 0.0)
    w_out_8 = mlp.make__dfloat(np.random.normal(), 0.0)

    params = [
        w_in_1,
        w_in_2,
        w_in_3,
        w_in_4,
        w_in_5,
        w_in_6,
        w_in_7,
        w_in_8,
        b_in_1,
        b_in_2,
        b_in_3,
        b_in_4,
        b_in_5,
        b_in_6,
        b_in_7,
        b_in_8,
        w_out_1,
        w_out_2,
        w_out_3,
        w_out_4,
        w_out_5,
        w_out_6,
        w_out_7,
        w_out_8,
    ]

    b_out = mlp.make__dfloat(np.random.normal(), 0.0)

    # plot
    x_axis = np.linspace(input_lower_bound, input_upper_bound, 100)
    init_result = [
        mlp.model(
            x,

            w_in_1.val, w_in_2.val, w_in_3.val, w_in_4.val,
            w_in_5.val, w_in_6.val, w_in_7.val, w_in_8.val,

            b_in_1.val, b_in_2.val, b_in_3.val, b_in_4.val,
            b_in_5.val, b_in_6.val, b_in_7.val, b_in_8.val,

            w_out_1.val, w_out_2.val, w_out_3.val, w_out_4.val,
            w_out_5.val, w_out_6.val, w_out_7.val, w_out_8.val,

            b_out.val,
        )
        for x in x_axis
    ]

    # end continuation
    def k(ret):
        ret.dval = 1
    
    # training loop
    eta = 1e-3

    def update(param):
        param.val -= eta * param.dval
        param.dval = 0.0
    
    for _ in range(num_training_steps):
        input_ = mlp.make__dfloat(np.random.uniform(low=input_lower_bound, high=input_upper_bound), 0.0)
        target = mlp.make__dfloat(target_func(input_.val), 0.0)

        mlp.d_loss(
            input_,

            w_in_1, w_in_2, w_in_3, w_in_4,
            w_in_5, w_in_6, w_in_7, w_in_8,

            b_in_1, b_in_2, b_in_3, b_in_4,
            b_in_5, b_in_6, b_in_7, b_in_8,

            w_out_1, w_out_2, w_out_3, w_out_4,
            w_out_5, w_out_6, w_out_7, w_out_8,

            b_out,

            target,

            k
        )

        [update(p) for p in params]

    # plot
    target = [target_func(x) for x in x_axis]
    final_result = [
        mlp.model(
            x,

            w_in_1.val, w_in_2.val, w_in_3.val, w_in_4.val,
            w_in_5.val, w_in_6.val, w_in_7.val, w_in_8.val,

            b_in_1.val, b_in_2.val, b_in_3.val, b_in_4.val,
            b_in_5.val, b_in_6.val, b_in_7.val, b_in_8.val,

            w_out_1.val, w_out_2.val, w_out_3.val, w_out_4.val,
            w_out_5.val, w_out_6.val, w_out_7.val, w_out_8.val,

            b_out.val,
        )
        for x in x_axis
    ]

    plt.plot(x_axis, target, label='target')
    plt.plot(x_axis, init_result, label='init')
    plt.plot(x_axis, final_result, label='final')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    train()