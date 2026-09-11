# Teoria passo a passo — aplicar relocations CLVM em C

Este laboratório é em **C + bytecode**. O arquivo `.clbc` já tem opcodes; você só corrige os **offsets u16 little-endian** quando o bloco de código muda de base.

## 1. O quê: relocação relativa

Uma relocação aqui não é ELF `R_X86_64_PC32`. É um patch de 2 bytes: em um site `at`, leia `u16` LE, some `delta` (com wrap 16-bit), grave de volta.

Por quê u16 e não i32? Na ISA CLVM deste portfolio, JMP/JZ/CALL/JNZ carregam deslocamento de 16 bits (opcode 1 + imm 2 = 3 bytes).

## 2. Como: layout no buffer

```text
índice | byte     | papel
-------|----------|------------------
0      | 0x09     | opcode JMP
1      | 0x0A     | offset lo (10)
2      | 0x00     | offset hi
3      | 0x08     | HALT (não relocável neste teste)
```

Site de relocação do JMP: `at = 1` (primeiro byte do imediato, **não** o opcode).

## 3. Trace numérico (Caso 2 do teste)

```text
antes:  09 0A 00 08
delta = +5
read u16 @1 = 0x0A | (0x00<<8) = 10
10 + 5 = 15 = 0x000F
grava lo=0x0F hi=0x00
depois: 09 0F 00 08
```

## 4. Por quê little-endian

O byte em `at` é o menos significativo. Se você gravar `15` só em `code[at]` e zerar `code[at+1]` por engano, o valor vira 15 — neste exemplo passa. O Caso 3 com sites `{1,4}` e valores 2 e 4 quebra se o hi-byte for corrompido.

## 5. Aplicar em lote (CLVM-RELOC-03)

```text
buf = 09 02 00 09 04 00
sites = [1, 4], delta = +3
site 1: 2+3 → 5 → bytes 05 00
site 4: 4+3 → 7 → bytes 07 00
resultado: 09 05 00 09 07 00
```

Se um site estiver OOB, a função retorna -1 **imediatamente** e não “pula” o site.

## 6. Wrap 16-bit (CLVM-RELOC-04)

```text
buf = FF FF
delta = +1
0xFFFF + 1 → 0x0000 (wrap uint16)
```

Por quê wrap e não saturar? Porque o linker educacional espelha aritmética modular do campo; saturação esconderia overflow do assembler.

## 7. Invariantes

- `reloc_read_u16` nunca lê além de `len`.
- Opcode em `at-1` não é modificado por `reloc_apply_one`.
- Ordem dos sites em `apply_all` é a ordem do array (esquerda → direita).

## 8. Bugs comuns

| Sintoma | Causa | Como ver |
|---------|-------|----------|
| v=2560 em vez de 10 | leu big-endian | `0x0A00` |
| OOB passa | não checou `at+2>len` | Caso 1 |
| site 4 não muda | loop com `i < n-1` | Caso 3 |
| wrap falha | usou `int` sem cast | Caso 4 |

## 9. Lab versus produção

ELF/PE usam tabelas de relocação com tipo e addend. Aqui a “tabela” é o array `sites[]` passado pelo teste — o mesmo papel, sem formato de arquivo.

## 10. Checklist

- [ ] Tracei 10+5=15 no papel
- [ ] Sei que o site aponta para o **imediato**, não para o opcode
- [ ] Sei que 0xFFFF+1 → 0

## Caderno de verificação — clvm_reloc_apply

Repita o trace do Caso 1 com os mesmos números do assert. Cada linha abaixo
fix um passo verificável; não invente outro exemplo.

1. Bytes `0A 00` em LE valem 10, não 2560.
2. Site do JMP está no índice 1.
3. Delta +5 produz `0F 00` no imediato.
4. Dois sites {1,4} com +3 produzem 5 e 7.
5. Wrap: `FF FF` +1 → `00 00`.

## Tabela de papéis

| Papel | Neste lab |
|-------|-----------|
| Entrada | fixture / buffer do Caso 1 |
| Transformação | corpo do TODO |
| Saída | valor comparado no assert |
| Erro | retorno negativo / false / Err |

## Fluxo

```text
fixture → bounds check → transformação → assert do teste
```

## Por quê falhar cedo

Erro de formato deve aparecer no retorno, não como valor default silencioso.

## Por quê o assert usa número fixo

O número fixo congela o contrato pedagógico; mudar o teste esconde o bug.

## Por quê não delegar ao gabarito

A RESOLUCAO traz o código completo; tente no starter antes de abrir solutions.

## Checklist final da teoria

- [ ] Trace do Caso 1 no papel
- [ ] Sei arquivo e função de cada TODO
- [ ] Sei o valor exato que o assert compara

