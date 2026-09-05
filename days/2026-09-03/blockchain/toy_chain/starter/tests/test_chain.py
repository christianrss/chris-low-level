// Test cases (TESTES_GUIADOS.md):
// Caso 1: Escreva um teste do comportamento mais simples antes de adicionar a feature.
// Caso 2: Rode e observe a falha.
// Caso 3: Implemente apenas o necessario para esse teste.
// Caso 4: Adicione edge case/erro relevante.
// Caso 5: Quando encontrar um bug durante o exercicio, transforme-o em regression test ant
# PEDAGOGY-TEST: CHAIN-DIGEST-01
# PEDAGOGY-TEST: CHAIN-MINE-01
# PEDAGOGY-TEST: CHAIN-MERKLE-01
# PEDAGOGY-TEST: CHAIN-VALID-01
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from toy_chain import ToyChain, merkle_root


def main():
    assert merkle_root(["a", "b"]) == merkle_root(["a", "b"])
    assert merkle_root(["a", "b"]) != merkle_root(["b", "a"])
    chain = ToyChain(difficulty=1)
    block = chain.append(["alice->bob:3"], 1)
    assert chain.valid()
    assert block.digest().startswith("0")
    chain.blocks[1].transactions[0] = "alice->mallory:3000"
    assert not chain.valid()
    print("toy chain tests passed")

if __name__ == "__main__": main()