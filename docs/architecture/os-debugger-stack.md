# Chris OS + Chris Debugger target architecture

Long-term data path:

`firmware -> chris-boot -> chris-kernel -> user mode -> window server/compositor -> chris-gui -> chris-desktop/apps`

Debug path:

`trap/breakpoint -> chris-kd-stub -> transport -> chris-kd-protocol -> chris-debugger -> chris-symbols/chris-dump`

Day 02 implements only the portable compositor reference and protocol framing. Future milestones deliberately preserve these portable implementations as test oracles for kernel/accelerated versions.
