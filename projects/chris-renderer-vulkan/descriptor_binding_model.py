class Layout:
 def __init__(self,required):
  # PEDAGOGY-SOLUTION: D8-GFX-LAYOUT
  if len(required)!=len(set(required)): raise ValueError('duplicate')
  if any(t not in {'uniform','texture','storage'} for t in required.values()): raise ValueError('type')
  self.required=dict(required)
class BindingState:
 def __init__(self,layout): self.layout=layout; self.bound={}
 def bind(self,binding,resource_type,name):
  # PEDAGOGY-SOLUTION: D8-GFX-BIND
  if binding not in self.layout.required: raise KeyError(binding)
  if self.layout.required[binding]!=resource_type: raise TypeError('descriptor type mismatch')
  self.bound[binding]=(resource_type,name); return True
 def validate_draw(self):
  # PEDAGOGY-SOLUTION: D8-GFX-DRAW
  missing=sorted(set(self.layout.required)-set(self.bound))
  if missing: raise RuntimeError(f'missing bindings: {missing}')
  ordered=[self.bound[i][1] for i in sorted(self.bound)]
  return {'vulkan':f'vkCmdBindDescriptorSets {ordered}','d3d12':f'SetGraphicsRootDescriptorTable {ordered}'}
