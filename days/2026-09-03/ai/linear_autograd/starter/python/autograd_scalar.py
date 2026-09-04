class Value:
    """Starter for a scalar computation graph."""

    def __init__(self, data: float) -> None:
        self.data = float(data)
        self.grad = 0.0
        self._prev = ()

    # TODO: implement __add__ and remember the operands.
    # TODO: implement __mul__ and remember the operands.
    # TODO: implement backward() with a topological traversal.


if __name__ == "__main__":
    x = Value(2.0)
    w = Value(3.0)
    b = Value(1.0)
    print("TODO: make y = w*x+b work, then add loss.backward()")
