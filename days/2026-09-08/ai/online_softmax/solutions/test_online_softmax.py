from online_softmax import *
# PEDAGOGY-TEST: D6-SM-STATS
# PEDAGOGY-TEST: D6-SM-NORMALIZE
a=online_softmax([1000.,1001.,999.]); assert abs(sum(a)-1)<1e-12
# PEDAGOGY-TEST: D6-SM-REFERENCE
b=softmax_two_pass([1000.,1001.,999.]); assert max(abs(x-y) for x,y in zip(a,b))<1e-12
assert online_softmax([0.,0.])==[0.5,0.5]
print("chris-online-softmax tests passed")
