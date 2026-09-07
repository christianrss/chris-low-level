TRANSITIONS={("PERCEIVE","perceived"):"PLAN",("PLAN","planned"):"ACT",("ACT","acted"):"OBSERVE",("OBSERVE","observed"):"VERIFY",("REVISE","revised"):"PLAN"}
class AgentFSM:
 def __init__(self,max_retries=2): self.state="PERCEIVE";self.max_retries=max_retries;self.retries=0;self.seq=0;self.trace=[];self.evidence=[]
 def transition(self,event):
  # PEDAGOGY-SOLUTION: D5-AGENT-TRANSITION
  key=(self.state,event)
  if key not in TRANSITIONS: raise ValueError(f"invalid transition {key}")
  old=self.state;self.state=TRANSITIONS[key];self.seq+=1;self.trace.append((self.seq,old,event,self.state));return self.state
 def verification(self,passed,evidence):
  # PEDAGOGY-SOLUTION: D5-AGENT-VERIFY
  if self.state!="VERIFY":raise ValueError("not verifying")
  self.evidence.append(evidence);old=self.state;self.seq+=1
  if passed:new="DONE";event="verified"
  elif self.retries<self.max_retries:self.retries+=1;new="REVISE";event="failed_verify"
  else:new="FAILED";event="retry_exhausted"
  self.state=new;self.trace.append((self.seq,old,event,new));return new
def replay(trace):
 # PEDAGOGY-SOLUTION: D5-AGENT-REPLAY
 state="PERCEIVE";expected=1
 for seq,old,event,new in trace:
  if seq!=expected or old!=state:raise ValueError("trace mismatch")
  if old=="VERIFY":
   if event not in ("verified","failed_verify","retry_exhausted"):raise ValueError("verify event")
   calc={"verified":"DONE","failed_verify":"REVISE","retry_exhausted":"FAILED"}[event]
  else:
   calc=TRANSITIONS.get((old,event))
  if calc!=new:raise ValueError("transition mismatch")
  state=new;expected+=1
 return state
