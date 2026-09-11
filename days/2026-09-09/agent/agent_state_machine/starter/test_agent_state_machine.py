from agent_state_machine import next_state, run, ToolResult

def test_transitions():
    # PEDAGOGY-TEST: D7-AGENT-TRANSITIONS
    assert next_state("PERCEIVE", "perceived") == "PLAN"
    try:
        next_state("DONE", "x")
        assert False
    except ValueError:
        pass

def test_run_trace():
    # PEDAGOGY-TEST: D7-AGENT-RUN
    # PEDAGOGY-TEST: D7-AGENT-TRACE
    def tool(task, retry):
        return ToolResult(ok=True, evidence="ok")
    state, trace = run("t", tool, lambda r: r.ok)
    assert state == "DONE"
    assert trace[0]["state"] == "PERCEIVE"
