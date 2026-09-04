from __future__ import annotations


def train(epochs: int = 1000, learning_rate: float = 0.01) -> tuple[float, float]:
    xs = [1.0, 2.0, 3.0, 4.0]
    ys = [3.0, 5.0, 7.0, 9.0]

    weight = 0.0
    bias = 0.0
    count = len(xs)

    for _ in range(epochs):
        d_weight = 0.0
        d_bias = 0.0

        for x, target in zip(xs, ys):
            prediction = weight * x + bias
            error = prediction - target

            # Manual backward pass for L=(prediction-target)^2.
            d_weight += 2.0 * error * x
            d_bias += 2.0 * error

        d_weight /= count
        d_bias /= count

        weight -= learning_rate * d_weight
        bias -= learning_rate * d_bias

    return weight, bias


if __name__ == "__main__":
    w, b = train()
    print(f"w={w:.6f} b={b:.6f}")
