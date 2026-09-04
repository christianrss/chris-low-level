# Research plan: software renderer vs GPU backend

Do not compare only FPS. Hold scene, resolution, camera and animation constant.

Record:

- resolution;
- triangle count;
- CPU frame time;
- GPU frame time where measurable;
- memory bandwidth/allocations if profiled;
- hardware and driver.

Early hypothesis: the software path will be dominated by per-pixel raster/depth work, while OpenGL shifts rasterization to the GPU and leaves CPU submission/scene work relatively small.
