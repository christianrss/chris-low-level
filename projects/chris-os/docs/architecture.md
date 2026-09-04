# Architecture - Day 02 reference layer

`Surface` is a CPU-owned RGBA image. `Layer` places one surface in screen coordinates. `Compositor::compose` walks layers in z-order and applies integer alpha-over blending.

Later the same abstraction will sit above a real framebuffer/display driver. The portable implementation remains as a golden reference path for testing accelerated backends.
