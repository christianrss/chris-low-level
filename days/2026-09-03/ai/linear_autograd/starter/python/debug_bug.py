"""Intentional backward-pass bugs for the debugging exercise."""

xs = [1.0, 2.0, 3.0, 4.0]
ys = [3.0, 5.0, 7.0, 9.0]

weight = 0.0
bias = 0.0
learning_rate = 0.01

for _ in range(1000):
    d_weight = 0.0
    d_bias = 0.0

    for x, target in zip(xs, ys):
        prediction = weight * x + bias
        error = prediction - target

        # BUGS INTENCIONAIS: descubra por que estes gradientes estão errados.
        d_weight += 2.0 * error
        d_bias += 2.0 * error * x

    weight -= learning_rate * d_weight
    bias -= learning_rate * d_bias

print(weight, bias)
