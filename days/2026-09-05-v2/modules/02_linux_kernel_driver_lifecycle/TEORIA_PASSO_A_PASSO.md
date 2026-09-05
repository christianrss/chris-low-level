# Teoria passo a passo

## 1. Driver de caractere como máquina de estados
Antes de trabalhar diretamente com kernel, modelamos `open/read/write/release` em C portátil. O objeto `Device` tem `is_open`, `buffer` e `length`. Isso permite estudar invariantes sem risco de travar a máquina.

## 2. Ownership e lifecycle
`device_open()` adquire o direito de uso exclusivo; um segundo open deve falhar. `device_release()` devolve esse estado. `device_write()` e `device_read()` só são válidos enquanto o dispositivo está aberto. Em kernel real, o mesmo raciocínio aparece em referências, locks, registradores, buffers DMA e recursos registrados em subsistemas.

## 3. Limites de buffer
O buffer possui 64 bytes. Uma implementação segura limita `count` antes de `memcpy`. No read, limite ao conteúdo disponível. Não confunda tamanho do buffer com tamanho válido (`length`).

## 4. Módulo real para revisão
`starter/chris_char.c` usa `misc_register()` em `chris_init()` e `misc_deregister()` em `chris_exit()`. Hoje ele não é carregado. O exercício é revisar a simetria init/exit. Em drivers reais, todo recurso adquirido precisa ter um caminho claro de cleanup, inclusive em falhas parciais de inicialização.

## 5. Próximo passo da trilha
Em dias futuros, esse modelo evolui para wait queues, concorrência, copy_to_user/copy_from_user, ioctl, poll e testes em VM/QEMU.