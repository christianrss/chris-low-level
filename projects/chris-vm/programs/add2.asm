# add2: 3+5 via procedure CALL/RET → imprime 8
# PEDAGOGY: CLVM-CALL-04
PUSH 3
PUSH 5
CALL add2
PRINT
HALT

add2:
ADD
RET
