"""Join barrier for parallel tool results."""
class ToolBarrier:
    def __init__(self, expected: int):
        # TODO [AGENT-JOIN-01]: store expected; results dict; done count
        raise NotImplementedError("AGENT-JOIN-01")

    def arrive(self, tool_id: str, payload: dict) -> bool:
        # TODO [AGENT-JOIN-02]: record result; return True when all arrived
        raise NotImplementedError("AGENT-JOIN-02")

    def snapshot(self) -> dict:
        # TODO [AGENT-JOIN-03]: return {done, expected, results}
        raise NotImplementedError("AGENT-JOIN-03")
