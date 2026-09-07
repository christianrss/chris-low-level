TRANSITIONS={("PERCEIVE","perceived"):"PLAN",("PLAN","planned"):"ACT",("ACT","acted"):"OBSERVE",("OBSERVE","observed"):"VERIFY",("REVISE","revised"):"PLAN"}
class AgentFSM:
 def __init__(self,max_retries=2): self.state="PERCEIVE";self.max_retries=max_retries;self.retries=0;self.seq=0;self.trace=[];self.evidence=[]
 def transition(self,event):
  # TODO [D5-AGENT-TRANSITION]: aplique tabela e registre trace.
  pass
 def verification(self,passed,evidence):
  # TODO [D5-AGENT-VERIFY]: DONE/REVISE/FAILED com retry guard.
  pass
def replay(trace):
 # TODO [D5-AGENT-REPLAY]: valide determinismo do controle.
 return None
