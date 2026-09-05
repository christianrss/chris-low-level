class Terminal:
    def __init__(self): self.fg=7; self.row=0; self.col=0; self.screen_text=''
    def _apply_csi(self,params,final):
        vals=[int(x) if x else 0 for x in params.split(';')] if params!='' else []
        if final=='m':
            if not vals: vals=[0]
            for v in vals:
                if v==0:self.fg=7
                elif v==31:self.fg=1
        elif final=='H':
            r=(vals[0] if len(vals)>0 and vals[0] else 1); c=(vals[1] if len(vals)>1 and vals[1] else 1); self.row=r-1; self.col=c-1
    def feed(self,text):
        i=0
        while i<len(text):
            if text.startswith('\x1b[',i):
                j=i+2
                while j<len(text) and text[j] not in 'mH': j+=1
                if j>=len(text): raise ValueError('truncated CSI')
                self._apply_csi(text[i+2:j],text[j]); i=j+1
            else: self.screen_text+=text[i]; self.col+=1; i+=1
