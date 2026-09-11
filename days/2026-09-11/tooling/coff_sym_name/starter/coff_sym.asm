; COFF symbol name field helpers — Windows x64 (RCX = ptr)
option casemap:none
.code
; TODO [TOOL-COFF-01]: return 1 if DWORD [rcx]==0 (long name), else 0
coff_name_is_long PROC
    xor eax, eax
    ret
coff_name_is_long ENDP
; TODO [TOOL-COFF-02]: return 1 if NOT long (short name in place)
coff_name_is_short PROC
    xor eax, eax
    ret
coff_name_is_short ENDP
; TODO [TOOL-COFF-03]: length of short name (strnlen up to 8)
coff_short_name_len PROC
    xor eax, eax
    ret
coff_short_name_len ENDP
END
