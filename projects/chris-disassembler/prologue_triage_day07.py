def triage(data:bytes):
    out={"push_rbp":False,"frame_pointer":False,"stack_reserve":0,"consumed":0};i=0
    # PEDAGOGY-SOLUTION: D7-X86-PUSH
    if i<len(data) and data[i]==0x55: out["push_rbp"]=True;i+=1
    # PEDAGOGY-SOLUTION: D7-X86-MOV
    if data[i:i+3]==b"\x48\x89\xe5": out["frame_pointer"]=True;i+=3
    # PEDAGOGY-SOLUTION: D7-X86-STACK
    if data[i:i+3]==b"\x48\x83\xec" and i+4<=len(data):out["stack_reserve"]=data[i+3];i+=4
    elif data[i:i+3]==b"\x48\x81\xec" and i+7<=len(data):out["stack_reserve"]=int.from_bytes(data[i+3:i+7],"little");i+=7
    out["consumed"]=i;return out
