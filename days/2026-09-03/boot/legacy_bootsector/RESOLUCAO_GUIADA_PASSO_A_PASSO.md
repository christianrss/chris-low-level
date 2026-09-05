# Resolucao guiada

## Mapa exato starter → resolução

| TODO ID | Starter | Função/área |
|---------|---------|-------------|
| `BOOT-IMAGE-01` | `starter/tools/build_minimal.py` | `build_image()` — bytes real-mode + assinatura `55 AA` |

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-03/boot/legacy_bootsector/starter/`. `solutions/` é o gabarito final e só deve ser consultado depois da tentativa.

1. Leia `src/bootsector.asm` e identifique `bits 16`, `org 0x7c00` e `dw 0xaa55`.
2. Em `tools/build_minimal.py`, escreva a sequencia de bytes correspondente as cinco instrucoes. Use o mapa de instrucoes em `TEORIA_PASSO_A_PASSO.md` (secao de encoding) — nao copie bytes sem conferir offset e opcode.
3. Crie um `bytearray(512)`, copie o codigo no inicio e escreva `55 aa` nos dois ultimos bytes.
4. O primeiro teste deve exigir exatamente 512 bytes; o segundo deve exigir a assinatura; o terceiro compara o prefixo de codigo.
5. Quando NASM/QEMU estiverem disponiveis, monte `bootsector.asm`, compare os bytes e execute em VM. Nao afirme que o boot foi testado em hardware nesta etapa.

## Etapa de código 1 - bytes de instrução

A sequência inicial deste laboratório é:

```text
B4 0E    mov ah, 0x0e
B0 48    mov al, 'H'
CD 10    int 0x10
F4       hlt
EB FD    jmp para o próprio loop
```

## Etapa de código 2 - construir imagem

```python
def build_image() -> bytes:
    code = bytes.fromhex("b4 0e b0 48 cd 10 f4 eb fd")
    image = bytearray(512)
    image[:len(code)] = code
    image[510:512] = b"\x55\xaa"
    return bytes(image)
```

## Etapa de teste

```python
image = build_image()
assert len(image) == 512
assert image[-2:] == b"\x55\xaa"
assert image[:9] == bytes.fromhex("b4 0e b0 48 cd 10 f4 eb fd")
```

O arquivo `solutions/src/bootsector.asm` mostra a versão NASM equivalente. NASM/QEMU não foram usados para afirmar execução neste ambiente; o teste deste milestone é estrutural/binário.

## 6. Depuração passo a passo

| Sintoma | Causa provável | Correção |
|---------|----------------|----------|
| `len != 512` | `bytearray` não preenchido até o fim | use `bytearray(512)` explícito |
| assinatura errada | bytes `AA 55` invertidos | últimos dois bytes: `\x55\xaa` |
| prefixo de código falha | hex incorreto ou ordem trocada | confira mapa `B4 0E B0 48 CD 10 F4 EB FD` |
| padding não zero | sobrescreveu bytes 9..509 | copie só `len(code)` bytes no início |

Inspecione manualmente:

```python
image = build_image()
print(image[0:9].hex(" "))
print(image[510:512].hex(" "))
```

## 7. Validação esperada

```bash
python starter/tests/test_boot.py
```

Saída: `boot image structural tests passed`.

## Mapa de consistência auditada

Cada TODO obrigatório do starter está mapeado abaixo. O identificador deve existir no starter, nesta resolução, na solução correspondente e na cobertura de testes/validação do módulo.

- `BOOT-IMAGE-01` — `starter/tools/build_minimal.py` → `solutions/tools/build_minimal.py`.

## Relatório de resolução

Checklist ao concluir:

- [ ] `BOOT-IMAGE-01` implementado em `starter/tools/build_minimal.py`.
- [ ] `python starter/tests/test_boot.py` passa (512 B, assinatura, código, padding).
- [ ] Bytes conferidos com `starter/src/bootsector.asm` (`bits 16`, `org 0x7c00`, `dw 0xaa55`).
- [ ] Se QEMU foi usado, resultado visual anotado separadamente do teste estrutural.

**Depuração:** compare `image[:9].hex()` com o mapa antes de alterar asserts dos testes.

**Arquivos starter editados:** `starter/tools/build_minimal.py`.
## Etapa de depuração

Se `len(image)!=512`, verifique padding. Se assinatura falhar, confira índices 510:512 (little-endian `55 AA`).

## Comparar com NASM

Quando disponível:

```bash
nasm -f bin bootsector.asm -o boot.bin
python -c "import pathlib; print(pathlib.Path('boot.bin').read_bytes()[:16].hex())"
```

Os primeiros bytes devem coincidir com a imagem Python.

## Perguntas de verificação

1. Por que o código começa em 0x7C00 e não 0x0000?
2. Qual o próximo estágio após este setor (stage2, FAT, GPT)?
3. Por que usamos `HLT` + `JMP` em vez de loop infinito simples?
