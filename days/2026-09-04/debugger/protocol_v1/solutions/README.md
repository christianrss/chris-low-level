# Chris Debugger

## Long-term goal
A first-party debugger for `chris-os`, including kernel-mode and user-mode debugging, symbols, unwinding, crash dumps and a graphical front end.

## Day 02 milestone
A portable **debug transport protocol codec**. Packets have a magic/version, command, request id, payload size and checksum. There is not yet a live kernel stub, so this milestone is deliberately described as protocol infrastructure rather than a working kernel debugger.

## Future architecture
`chris-kd-stub` in the kernel ↔ serial/virtio/TCP transport ↔ `chris-debugger` host ↔ `chris-symbols`/`chris-dump`.

## Safety
The project is designed for the user's own OS/processes and controlled VMs.
