from dataclasses import dataclass
STATES=["PERCEIVE","PLAN","ACT","OBSERVE","VERIFY","REVISE","DONE","FAILED"]
@dataclass(frozen=True)
class ToolResult: ok:bool; evidence:str
def next_state(state,event):
    # PEDAGOGY-SOLUTION: D7-AGENT-TRANSITIONS
    m={("PERCEIVE","perceived"):"PLAN",("PLAN","planned"):"ACT",("ACT","acted"):"OBSERVE",("OBSERVE","observed"):"VERIFY",("VERIFY","passed"):"DONE",("VERIFY","failed"):"REVISE",("REVISE","revised"):"ACT",("VERIFY","exhausted"):"FAILED"}
    if (state,event) not in m:raise ValueError("invalid transition")
    return m[(state,event)]
def run(task,tool,verify,max_retries=2):
    # PEDAGOGY-SOLUTION: D7-AGENT-RUN
    # PEDAGOGY-SOLUTION: D7-AGENT-TRACE
    state="PERCEIVE";trace=[];retry=0
    def step(event,data):
        nonlocal state
        trace.append({"state":state,"event":event,"data":data});state=next_state(state,event)
    step("perceived",{"task":task});step("planned",{"summary":"attempt task"})
    while True:
        result=tool(task,retry);step("acted",{"retry":retry,"ok":result.ok});step("observed",{"evidence":result.evidence})
        if verify(result):step("passed",{"verified":True});return state,trace
        if retry>=max_retries:step("exhausted",{"verified":False});return state,trace
        step("failed",{"verified":False});retry+=1;step("revised",{"retry":retry})
