import subprocess
def split_items(data,nul=False):
    # PEDAGOGY-SOLUTION: D6-XARGS-SPLIT
    return [x for x in data.split("\0") if x!=""] if nul else data.split()
def batches(items,n):
    # PEDAGOGY-SOLUTION: D6-XARGS-BATCH
    if n<=0: raise ValueError("n")
    return [items[i:i+n] for i in range(0,len(items),n)]
def run_batches(command,items,n):
    # PEDAGOGY-SOLUTION: D6-XARGS-RUN
    for batch in batches(items,n):
        cp=subprocess.run(command+batch,shell=False)
        if cp.returncode!=0: return cp.returncode
    return 0
