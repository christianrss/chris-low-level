# Teoria passo a passo — Linux kernel: lifecycle de char device + módulo real para revisão

Drivers de caractere expõem uma interface de bytes/controle por `struct file_operations`. O kernel chama callbacks como `open`, `read`, `write` e `release`; o driver precisa manter invariantes de lifetime, tamanho e concorrência.

Para separar aprendizado de risco, o starter possui **dois artefatos**: `device_model.c`, um modelo userspace totalmente testável, e `chris_char.c`, fonte de módulo de kernel para leitura guiada. Neste ambiente não há headers/toolchain de kernel preparados e o módulo NÃO será carregado.

O modelo portátil simula um device com buffer de 64 bytes, flag `is_open` e `length`. `open` falha se já aberto; write exige device aberto e limita o tamanho; read copia até `length`. Essa disciplina prepara o raciocínio de error paths e ownership que será necessário no kernel real.
