from __future__ import annotations


def train(epochs: int = 1000, learning_rate: float = 0.01) -> tuple[float, float]:
    xs = [1.0, 2.0, 3.0, 4.0]
    ys = [3.0, 5.0, 7.0, 9.0]

    weight = 0.0
    bias = 0.0

    for _ in range(epochs):
        d_weight = 0.0
        d_bias = 0.0

        for x, target in zip(xs, ys):
            prediction = weight * x + bias
            error = prediction - target

            # TODO [AI-PY-GRAD-01]: derive dL/dw and dL/db and accumulate them.
            _ = (x, error)

        # TODO [AI-PY-SGD-01]: average gradients and update weight/bias using SGD.
        _ = (d_weight, d_bias, learning_rate)

    return weight, bias


if __name__ == "__main__":
    w, b = train()
    print(f"w={w:.6f} b={b:.6f}")
