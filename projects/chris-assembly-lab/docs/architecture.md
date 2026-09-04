# ABI Notes

System V AMD64 passes the first pointer argument in `RDI` and the second integer argument in `RSI`; integer return values use `RAX`. The function touches only caller-saved registers, so it needs no stack frame.
