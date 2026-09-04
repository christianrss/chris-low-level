; Legacy BIOS boot sector equivalent to tools/build_minimal.py
bits 16
org 0x7c00

start:
    mov ah, 0x0e
    mov al, 'H'
    int 0x10
    hlt
hang:
    jmp hang

times 510 - ($ - $$) db 0
dw 0xaa55
