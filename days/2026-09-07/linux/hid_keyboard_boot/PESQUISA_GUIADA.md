# Pesquisa guiada — HID boot keyboard → InputEvent

Leia a documentação do kernel sobre **HID boot protocol**, `struct input_event` em `uapi/linux/input.h`, e `Documentation/hid/hid-input.rst` (ou equivalente). Pesquise também `evtest` e `libevdev`.

Perguntas:
1. Qual a diferença entre relatório HID **boot** e **report protocol**?
2. Por que `input_sync()` é necessário após `input_report_key()`?
3. Como o kernel evita perder eventos quando userspace não lê rápido?
4. O que `EV_SYN` / `SYN_REPORT` significa?

## Regra
Use as fontes para **entender e validar**. Não copie implementação pronta para o starter. Registre o que aprendeu e qual decisão do exercício a fonte justifica.

## Registro do aluno

| Pergunta | Sua resposta (3–5 linhas) | Decisão no código |
|----------|---------------------------|-------------------|
| Boot vs report protocol | | |
| input_sync | | |
| Backpressure / buffer | | |
| EV_SYN | | |

## Checkpoint

Antes de implementar `TODO [HID-KBD-DECODE-01]`, explique o layout dos 8 bytes **sem olhar a resolução**. Registre no Relatório de resolução.
