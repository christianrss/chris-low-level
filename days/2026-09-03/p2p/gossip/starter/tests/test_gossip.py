// Test cases (TESTES_GUIADOS.md):
// Caso 1: Escreva um teste do comportamento mais simples antes de adicionar a feature.
// Caso 2: Rode e observe a falha.
// Caso 3: Implemente apenas o necessario para esse teste.
// Caso 4: Adicione edge case/erro relevante.
// Caso 5: Quando encontrar um bug durante o exercicio, transforme-o em regression test ant
# PEDAGOGY-TEST: P2P-GOSSIP-01
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from gossip import GossipNetwork, Message


def main():
    net = GossipNetwork()
    net.connect("a", "b"); net.connect("b", "c"); net.connect("c", "a")
    reached = net.broadcast("a", Message("m1", "hello", ttl=8))
    assert reached == {"a", "b", "c"}
    assert len([x for x in net.deliveries if x[1] == "m1"]) == 3

    line = GossipNetwork()
    line.connect("a", "b"); line.connect("b", "c"); line.connect("c", "d")
    assert line.broadcast("a", Message("m2", "x", ttl=1)) == {"a", "b"}
    print("gossip tests passed")

if __name__ == "__main__": main()