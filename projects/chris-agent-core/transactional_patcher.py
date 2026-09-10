import hashlib
def apply_hunk(text,old,new):
 # PEDAGOGY-SOLUTION: D8-PATCH-HUNK
 c=text.count(old)
 if c!=1: raise ValueError(f'hunk match count={c}')
 return text.replace(old,new,1)
def apply_transaction(workspace,patches):
 # PEDAGOGY-SOLUTION: D8-PATCH-TXN
 staging=dict(workspace); trace=[]
 for p in patches:
  path=p['path']
  if path not in staging: raise FileNotFoundError(path)
  before=staging[path]; after=apply_hunk(before,p['old'],p['new']); staging[path]=after
  # PEDAGOGY-SOLUTION: D8-PATCH-TRACE
  h=lambda s: hashlib.sha256(s.encode()).hexdigest()
  trace.append({'path':path,'old_sha256':h(before),'new_sha256':h(after),'bytes_delta':len(after.encode())-len(before.encode())})
 # PEDAGOGY-SOLUTION: D8-PATCH-COMMIT
 workspace.clear();workspace.update(staging);return trace
