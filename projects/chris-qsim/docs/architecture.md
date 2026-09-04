# Architecture

Basis index bits encode qubit values. A single-qubit gate visits amplitude pairs whose indices differ in one target bit. CNOT swaps pairs only when the control bit is one. This direct mapping makes memory traffic visible for later optimization work.
