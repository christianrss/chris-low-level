from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
module_path = ROOT / "python" / "linear_train.py"
spec = importlib.util.spec_from_file_location("linear_train", module_path)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

weight, bias = module.train()
assert abs(weight - 2.0) < 0.02, weight
assert abs(bias - 1.0) < 0.05, bias
print("AI tests: PASS")
