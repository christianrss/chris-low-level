"""Optional comparison only: verifies the manual gradient using PyTorch.

The low-level implementation remains the primary exercise. This script is
intentionally optional and exits with a clear message when torch is absent.
"""

try:
    import torch
except ImportError as exc:
    raise SystemExit(
        "PyTorch is not installed. This comparison is optional; "
        "the manual Python/C exercises require no framework."
    ) from exc


# Build the same scalar example used by the manual exercise.
x = torch.tensor(2.0)
weight = torch.tensor(3.0, requires_grad=True)
bias = torch.tensor(1.0, requires_grad=True)
target = torch.tensor(10.0)

prediction = weight * x + bias
loss = (prediction - target) ** 2
# PyTorch records the graph during forward and walks it in reverse here.
loss.backward()

print(f"prediction={prediction.item():.1f} loss={loss.item():.1f}")
print(f"dL/dw={weight.grad.item():.1f} dL/db={bias.grad.item():.1f}")
