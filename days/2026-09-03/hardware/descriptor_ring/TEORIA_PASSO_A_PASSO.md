# Teoria passo a passo - descriptor rings

Muitos dispositivos de rede, storage e GPU trocam trabalho por filas circulares de descriptors. O software prepara descriptors; muda ownership; o dispositivo processa; depois devolve ownership/completion. Em hardware real, descriptors podem ser vistos via DMA e registradores MMIO apontam para filas.

Neste laboratorio nao ha DMA/MMIO real. Modelamos apenas as invariantes de produtor, device cursor e consumidor, que sao a parte conceitual mais importante antes de escrever um driver virtio/e1000.
