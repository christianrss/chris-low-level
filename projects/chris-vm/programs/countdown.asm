# Prints 3, 2, 1, 0 using relative branches.
PUSH 3
loop:
DUP
PRINT
PUSH 1
SUB
DUP
JZ end
JMP loop
end:
PRINT
HALT
