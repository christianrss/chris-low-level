# Experiment: finite-difference gradient checking

**Question:** how does finite-difference epsilon affect agreement with the analytical/autograd gradient?

**Hypothesis:** very large epsilon increases truncation error, while very small epsilon eventually increases floating-point cancellation error.

Future experiment: sweep epsilon from `1e-1` to `1e-12`, record absolute/relative error and compare float32 vs float64.
