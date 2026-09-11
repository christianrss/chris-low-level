from tool_barrier_join import ToolBarrier
# PEDAGOGY-TEST: AGENT-JOIN-01
def test_init():
    b = ToolBarrier(2)
    assert b.expected == 2 and b.done == 0
# PEDAGOGY-TEST: AGENT-JOIN-02
def test_arrive():
    b = ToolBarrier(2)
    assert b.arrive("a", {"v": 1}) is False
    assert b.arrive("b", {"v": 2}) is True
# PEDAGOGY-TEST: AGENT-JOIN-03
def test_snap():
    b = ToolBarrier(2)
    b.arrive("a", {"v": 1})
    s = b.snapshot()
    assert s["done"] == 1 and s["expected"] == 2 and s["results"]["a"]["v"] == 1

if __name__ == "__main__":
    test_init(); test_arrive(); test_snap(); print("ok")
