# Day 03 architecture

Linux distro track: `chris-linux-build` monta rootfs e `chris-linux-pkg` instala packages no staging root. Kernel track aprende lifetime em modelo portátil antes de módulo real. Graphics track cria vocabulário comum para resource states que depois alimentará backends Vulkan e D3D12.

A estratégia continua vertical: componentes pequenos, invariantes testáveis, depois integração.
