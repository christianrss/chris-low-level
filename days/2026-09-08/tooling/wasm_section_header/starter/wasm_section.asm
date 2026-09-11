; WASM magic / version / section id — Windows x64 (RCX = pointer or id)
option casemap:none
.code
; TODO [TOOL-WASM-01]: return 1 if bytes 00 61 73 6D
wasm_magic_ok PROC
    xor eax, eax
    ret
wasm_magic_ok ENDP
; TODO [TOOL-WASM-02]: version u32 LE at +4 equals 1
wasm_version_is_1 PROC
    xor eax, eax
    ret
wasm_version_is_1 ENDP
; TODO [TOOL-WASM-03]: section id in CL: 1 type, 2 import, else 0
section_class PROC
    xor eax, eax
    ret
section_class ENDP
END
