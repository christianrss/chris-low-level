# Resolucao guiada

1. Leia `src/bootsector.asm` e identifique `bits 16`, `org 0x7c00` e `dw 0xaa55`.
2. Em `tools/build_minimal.py`, escreva a sequencia de bytes correspondente as cinco instrucoes. Nao copie sem conferir no mapa fornecido no DOCX.
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

