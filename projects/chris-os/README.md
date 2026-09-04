# Chris OS

## Long-term goal
Build a complete operating system from boot to graphical desktop, drivers, networking, userland and a first-party debugger.

## Day 02 milestone
A **host-side graphics reference model**: RGBA surfaces, clipped rectangle drawing, layer placement and alpha compositing. This is intentionally not called a kernel or a bootable OS yet. It gives the future window server a correctness oracle that can be tested on any host.

## Why start this way?
Kernel graphics code is difficult to diagnose. A portable reference implementation lets us define pixel-level golden tests before moving the same concepts behind a framebuffer/virtio-gpu driver.

## Next milestones
- bootable kernel and serial console integration;
- framebuffer abstraction;
- input events;
- shared surfaces/window server;
- graphical desktop;
- user/kernel process model;
- integration with `chris-debugger`.
