# Teoria passo a passo — primeiro boot sector legado (PC real-mode)

## 1. O que estamos construindo

Uma imagem de boot de 512 bytes que o firmware legado pode carregar no endereço físico `0x7C00` e executar em modo real 16-bit. O programa imprime `'H'` via BIOS `int 0x10` e entra em loop com `HLT`.

## 2. Por que 512 bytes e assinatura 0xAA55

O setor de boot clássico tem exatamente 512 bytes. Os bytes 510–511 devem ser `0x55 0xAA` (little-endian da palavra `0xAA55`). Sem isso, o BIOS não reconhece o setor como bootável.

```text
offset 0x000 .. 0x1FD : código + padding
offset 0x1FE .. 0x1FF : 55 AA
```

## 3. Layout da imagem (tabela de offsets)

```text
offset | conteúdo
-------|----------------------------------
0x00   | B4 0E  mov ah, 0x0E  (teletype)
0x02   | B0 48  mov al, 'H'
0x04   | CD 10  int 0x10       (BIOS video)
0x06   | F4     hlt
0x07   | EB FD  jmp cur-1        (loop infinito)
0x09.. | 0x00   padding
0x1FE  | 0x55
0x1FF  | 0xAA
```

## 4. Como funciona internamente

Modo real: segmento CS aponta para `0x7C00`, IP inicia em 0. `org 0x7c00` no NASM alinha labels com o endereço físico.

`int 0x10` com `AH=0x0E` imprime o caractere em `AL` na posição do cursor (teletype).

`HLT` para a CPU até interrupção; `jmp $` mantém o processador ocupado se o HLT não for suficiente na VM.

## 5. Exemplo numérico — construção Python

```python
code = bytes.fromhex("b4 0e b0 48 cd 10 f4 eb fd")  # 9 bytes
image = bytearray(512)
image[:9] = code
image[510:512] = b"\x55\xaa"
assert len(image) == 512
```

Bytes `9..509` permanecem zero — padding válido.

## 6. Invariantes

- `len(image) == 512` sempre.
- Assinatura nos últimos dois bytes, não no início.
- Código real-mode: não usar instruções de 32/64 bits sem prefixos adequados.
- `build_image()` determinístico: mesma entrada → mesmos bytes.

## 7. Complexidade

- Construção da imagem: O(512) = O(1) fixo.
- Não há loop de dados; boot é O(1) até HLT.

## 8. Bugs comuns

- Assinatura `AA 55` invertida (big-endian errado).
- Imagem menor que 512 bytes.
- Copiar código NASM sem conferir bytes no mapa.
- Esquecer padding entre código e assinatura.
- Afirmar teste em hardware real quando só validação estrutural rodou.

## 9. Comparação com produção

| Este lab | Boot moderno (UEFI) |
|----------|---------------------|
| 512 B MBR sector | GPT + EFI System Partition |
| modo real 16-bit | modo longo 64-bit |
| BIOS `int 0x10` | GOP/UEFI protocols |
| setor único | bootloader multi-stage |

O princípio permanece: firmware carrega bytes iniciais e transfere controle.

## 10. Passo a passo guiado

1. Leia `starter/src/bootsector.asm`: `bits 16`, `org 0x7c00`, `dw 0xaa55`.
2. Complete `starter/tools/build_minimal.py` (`BOOT-IMAGE-01`).
3. Rode `python starter/tests/test_boot.py`.
4. Opcional: NASM + QEMU para execução visual.

## 11. Como saber se está correto

```text
boot image structural tests passed
```

512 bytes, assinatura correta, prefixo de código `b4 0e b0 48 cd 10 f4 eb fd`, padding zero no meio.
## 6. Mapa de memória no boot

```text
0x0000_0000  BIOS data / IVT
0x0000_7C00  Setor de boot carregado (512 bytes)
0x0000_7DFE  Assinatura 0xAA55 (bytes 510-511)
```

## 7. Fluxo de execução real-mode

```text
Power-on -> BIOS POST -> int 19h -> carrega setor 0 -> salta 0x7C00
                                              |
                                              v
                                    código do aluno (16-bit)
```

## 8. INT 0x10 — teletype

`AH=0x0E`, `AL=caractere` imprime via BIOS. É lento, mas não exige buffer de vídeo manual.

## 9. Invariantes do setor

| Invariante | Valor |
|------------|-------|
| Tamanho total | 512 bytes |
| Assinatura | `55 AA` nos offsets 510-511 |
| Modo inicial | real mode, CS:IP = 0000:7C00 |

## 10. Bugs comuns

- Esquecer `org 0x7C00` no NASM (endereços errados).
- Colocar assinatura no offset errado.
- Usar instruções 32-bit sem prefixo em modo 16-bit.
- Confundir imagem Python com binário NASM sem comparar bytes.

## 11. QEMU sanity (opcional)

```bash
qemu-system-x86_64 -drive format=raw,file=boot.img
```

Se não tiver QEMU, os testes estruturais Python ainda validam o layout.

## 12. Por que 512 bytes?

Setor físico legacy de disquete/HD em modo CHS. O BIOS transfere exatamente um setor para 0x7C00.

---

## Por quê — síntese pedagógica

### Por quê este módulo existe?
Conectar teoria de baixo nível a decisões de implementação verificáveis — não decorar API.

### Por quê estas invariantes?
Cada `TODO [ID]` protege uma propriedade que quebra silenciosamente em produção se ignorada (overflow, estado inválido, parsing parcial).

### Por quê medir e portar para `projects/`?
Lab isola o aprendizado; `projects/chris-*` consolida engenharia de portfólio com testes e benchmarks reproduzíveis.
