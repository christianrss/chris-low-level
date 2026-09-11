"""Join barrier for parallel tool results."""
class ToolBarrier:
    def __init__(self, expected: int):
        # PEDAGOGY-SOLUTION: AGENT-JOIN-01
        if expected <= 0:
            raise ValueError("expected")
        self.expected = expected
        self.results: dict[str, dict] = {}
        self.done = 0

    def arrive(self, tool_id: str, payload: dict) -> bool:
        # PEDAGOGY-SOLUTION: AGENT-JOIN-02
        if tool_id in self.results:
            return self.done >= self.expected
        self.results[tool_id] = payload
        self.done += 1
        return self.done >= self.expected

    def snapshot(self) -> dict:
        # PEDAGOGY-SOLUTION: AGENT-JOIN-03
        return {"done": self.done, "expected": self.expected, "results": dict(self.results)}
