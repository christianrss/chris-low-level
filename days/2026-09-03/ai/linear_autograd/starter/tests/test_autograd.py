// Test cases (TESTES_GUIADOS.md):
// Caso 1: Importe `train()`.
// Caso 2: Execute 1000 épocas com `lr=0.01`.
// Caso 3: Use tolerâncias em vez de igualdade exata porque treinamento usa ponto flutuante
// Caso 4: Verifique `abs(w-2) < 0.02` e `abs(b-1) < 0.05`.
# PEDAGOGY-TEST: AI-PY-GRAD-01
# PEDAGOGY-TEST: AI-PY-SGD-01
# PEDAGOGY-TEST: AI-AUTOGRAD-BWD-01
# PEDAGOGY-TEST: AI-AUTOGRAD-ADD-01
# PEDAGOGY-TEST: AI-AUTOGRAD-MUL-01
# PEDAGOGY-TEST: AI-C-GRAD-01
# PEDAGOGY-TEST: AI-C-SGD-01
# PEDAGOGY-TEST: AI-C-AVG-01
from __future__ import annotations
import math, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'python'))
from autograd_scalar import Value
from linear_train import train

def test_convergence() -> None:
    w,b=train()
    assert abs(w-2.0)<0.02
    assert abs(b-1.0)<0.05

def scalar_loss(w: float, x: float=2.0, b: float=1.0, y: float=10.0) -> float:
    e=w*x+b-y
    return e*e

def test_gradient_check() -> None:
    x=Value(2.0); w=Value(3.0); b=Value(1.0); target=Value(10.0)
    loss=(w*x+b-target)**2
    loss.backward()
    eps=1e-6
    numeric=(scalar_loss(3.0+eps)-scalar_loss(3.0-eps))/(2*eps)
    assert math.isclose(w.grad, numeric, rel_tol=1e-6, abs_tol=1e-5)

def test_gradient_accumulates() -> None:
    x=Value(3.0)
    z=x*x+x
    z.backward()
    assert math.isclose(x.grad, 7.0, rel_tol=0, abs_tol=1e-9)

def test_unsupported_power() -> None:
    try:
        _=Value(2.0)**3
    except ValueError:
        return
    raise AssertionError('power=3 should be rejected')

def main() -> int:
    for f in [test_convergence,test_gradient_check,test_gradient_accumulates,test_unsupported_power]: f()
    print('chris-autograd tests passed'); return 0
if __name__=='__main__': raise SystemExit(main())