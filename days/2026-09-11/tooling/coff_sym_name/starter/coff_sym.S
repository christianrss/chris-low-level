# GAS Linux SYSV: rdi = ptr
.global coff_name_is_long
.global coff_name_is_short
.global coff_short_name_len
.text
# TODO [TOOL-COFF-01]
coff_name_is_long:
    xor %eax, %eax
    ret
# TODO [TOOL-COFF-02]
coff_name_is_short:
    xor %eax, %eax
    ret
# TODO [TOOL-COFF-03]
coff_short_name_len:
    xor %eax, %eax
    ret
