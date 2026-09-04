# Corrected reference implementation for the intentional backward-pass bug.
\
"""Reference correction for the backward-pass debugging exercise."""

xs = [1.0, 2.0, 3.0, 4.0]
ys = [3.0, 5.0, 7.0, 9.0]

weight = 0.0
bias = 0.0
learning_rate = 0.01
count = len(xs)

for _ in range(1000):
    d_weight = 0.0
    d_bias = 0.0

    for x, target in zip(xs, ys):
        prediction = weight * x + bias
        error = prediction - target
        d_weight += 2.0 * error * x
        d_bias += 2.0 * error

    d_weight /= count
    d_bias /= count

    weight -= learning_rate * d_weight
    bias -= learning_rate * d_bias

print(f"w={weight:.6f} b={bias:.6f}")
