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
