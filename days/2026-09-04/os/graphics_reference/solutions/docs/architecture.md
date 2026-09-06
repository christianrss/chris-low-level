# Architecture - Day 02 reference layer

`Surface` is a CPU-owned RGBA image with an embedded `DirtyTracker`. `Layer` places one surface in screen coordinates. `Compositor::compose` walks layers in z-order, applies integer alpha-over blending, and marks each layer footprint dirty.

`DirtyTracker` maintains a single AABB union of changed regions (`mark_dirty` / `take_dirty_union`). `FramePacer::compose_with_damage` recomposes only that region into an existing framebuffer and reports `FrameStats {pixels_touched, dirty_area}` — the pedagogical stand-in for vsync/frame-pacing cost before a real display pipeline.

Later the same abstraction will sit above a real framebuffer/display driver. The portable implementation remains as a golden reference path for testing accelerated backends and damage protocols.
