def run(code,text,max_steps=100000):
 # PEDAGOGY-SOLUTION: D8-BT-VM
 stack=[(0,0)]; steps=0
 while stack:
  pc,pos=stack.pop()
  while True:
   # PEDAGOGY-SOLUTION: D8-BT-LIMIT
   steps+=1
   if steps>max_steps: raise RuntimeError('step limit')
   op=code[pc]; kind=op[0]
   if kind=='CHAR':
    if pos>=len(text) or text[pos]!=op[1]: break
    pc+=1;pos+=1
   elif kind=='JMP': pc=op[1]
   elif kind=='SPLIT':
    # PEDAGOGY-SOLUTION: D8-BT-SPLIT
    stack.append((op[2],pos));pc=op[1]
   elif kind=='MATCH': return (pos==len(text)),steps
   else: raise ValueError(kind)
 return False,steps
