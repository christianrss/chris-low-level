# Pesquisa guiada — Linux kernel: lifecycle de char device + módulo real para revisão

Leia documentação oficial do kernel sobre “Character devices”/driver model e pesquise `misc_register file_operations`. Perguntas: o que `copy_to_user` protege? Por que não se deve usar `memcpy` diretamente para um ponteiro userspace? O que acontece se init adquire recurso e exit não libera?

## Regra
Use as fontes para **entender e validar**. Não copie uma implementação pronta para preencher o starter. Registre em poucas linhas o que aprendeu e qual decisão do exercício a fonte ajuda a justificar.
