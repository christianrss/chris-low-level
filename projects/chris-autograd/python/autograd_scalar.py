from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass(eq=False)
class Value:
    data: float
    label: str = ""
    grad: float = 0.0
    _prev: tuple["Value", ...] = field(default_factory=tuple, repr=False)
    _backward: Callable[[], None] = field(
        default=lambda: None,
        repr=False,
    )

    def __add__(self, other: "Value | float") -> "Value":
        rhs = other if isinstance(other, Value) else Value(float(other))
        out = Value(self.data + rhs.data, _prev=(self, rhs))

        def backward() -> None:
            # d(a+b)/da = 1 and d(a+b)/db = 1.
            self.grad += out.grad
            rhs.grad += out.grad

        out._backward = backward
        return out

    def __mul__(self, other: "Value | float") -> "Value":
        rhs = other if isinstance(other, Value) else Value(float(other))
        out = Value(self.data * rhs.data, _prev=(self, rhs))

        def backward() -> None:
            # Product rule for the local derivatives.
            self.grad += rhs.data * out.grad
            rhs.grad += self.data * out.grad

        out._backward = backward
        return out

    def __sub__(self, other: "Value | float") -> "Value":
        rhs = other if isinstance(other, Value) else Value(float(other))
        return self + (rhs * -1.0)

    def __pow__(self, power: int) -> "Value":
        if power != 2:
            raise ValueError("this educational Value only implements power=2")

        out = Value(self.data * self.data, _prev=(self,))

        def backward() -> None:
            self.grad += 2.0 * self.data * out.grad

        out._backward = backward
        return out

    def backward(self) -> None:
        topo: list[Value] = []
        visited: set[Value] = set()

        def build(node: Value) -> None:
            if node in visited:
                return
            visited.add(node)
            for parent in node._prev:
                build(parent)
            topo.append(node)

        build(self)
        self.grad = 1.0

        for node in reversed(topo):
            node._backward()


def demo() -> None:
    x = Value(2.0, label="x")
    weight = Value(3.0, label="w")
    bias = Value(1.0, label="b")
    target = Value(10.0, label="target")

    prediction = weight * x + bias
    error = prediction - target
    loss = error ** 2
    loss.backward()

    print(f"prediction={prediction.data:.1f} loss={loss.data:.1f}")
    print(f"dL/dw={weight.grad:.1f} dL/db={bias.grad:.1f}")


if __name__ == "__main__":
    demo()
