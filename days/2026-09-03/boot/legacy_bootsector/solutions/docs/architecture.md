# Architecture

Legacy BIOS loads the selected boot sector at physical address 0x7C00 and transfers control in 16-bit real mode. The final two bytes `55 AA` are the traditional boot signature. This milestone intentionally stops before disk I/O, GDT or protected mode.
