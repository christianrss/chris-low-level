# Teoria passo a passo — Debug protocol v1

## 1. O problema de produção

Debuggers trocam mensagens compactas entre host e stub. Texto livre é frágil; layout binário fixo permite validar **antes** de interpretar payload. Este módulo é o wire format do futuro `chris-debugger`.

### O quê

Serialização LE (`append`/`read` u16/u32), checksum FNV-1a do payload, `encode_debug_packet` / `decode_debug_packet` com header de 20 bytes.

### Como

Escrever magic→version→command→request_id→payload_size→hash→bytes. Decode fail-fast: tamanho ≥20 → magic → version → campos → `size == 20+payload_size` → hash.

### Por quê

Length mentiroso sem checagem = buffer overrun lógico / DoS. Hash no header sem validar tamanho = trabalho inútil em pacote truncado. FNV-1a detecta corrupção acidental — **não** autentica (sem MAC/TLS).

## 2. Layout (20 B + N)

```text
0   4  magic "CKD1" (0x31444B43 LE)
4   2  version
6   2  command
8   4  request_id
12  4  payload_size
16  4  FNV-1a(payload)
20  N  payload
```

## 3. Little-endian

| Op | Entrada | Bytes |
|----|---------|-------|
| append_u16(0x0102) | 258 | 02 01 |
| append_u32(5) | 5 | 05 00 00 00 |
| read_u16 [34,12] | — | 0x1234 |

Magic CKD1 wire: `43 4B 44 31`.

## 4. FNV-1a

```text
hash = 2166136261
para cada byte b: hash ^= b; hash *= 16777619
```

Não é cripto. Produção crítica usa MAC/AEAD.

## 5. Encode / decode

Encode: rejeitar payload > 1 MiB; reserve; append campos; hash só do payload; concatena.

Decode (ordem):

```text
1 size>=20  2 magic  3 version  4 ler campos
5 size==20+N  6 copiar payload  7 hash  8 comparar
```

## 6. Invariantes

| Invariante | Motivo |
|------------|--------|
| `kHeaderSize==20` | layout fixo |
| hash só payload | contrato |
| limite 1 MiB | anti-DoS |
| version explícita | evolução |

## 7. Bugs clássicos

1. BE no wire.
2. Hash incluir header.
3. Aceitar `payload_size` gigante sem checar `bytes.size()`.
4. Copiar payload antes de validar tamanho total.
5. Tratar FNV como autenticação.

## 8. Comparação

| | v1 | GDB RSP | LLDB |
|--|----|---------|------|
| Formato | binário fixo | texto+bin | packets |
| Integridade | FNV-1a | opcional | checksums |

## 9. Arquitetura futura

```text
chris-kd-stub (kernel)
  <-> serial / virtio / TCP
  <-> protocolo v1 (este módulo)
  <-> host chris-debugger
```

## 10. Ataques parciais

| Ataque | Mitigação v1 |
|--------|--------------|
| Truncado | size checks |
| Length mentiroso | `== 20+N` |
| Corrupção | FNV-1a |
| Replay/MITM | **não** |

## 11. Perguntas

1. Por que magic antes de ler `payload_size`?
2. O que faz `payload_size=0`?
3. Por que FNV não basta em rede hostil?

## Fundamentos adicionais (reforço Dia 01)

### O quê

Um protocolo de debugger serializa comandos e respostas em frames com checksum para sobrevivência a truncamento.

### Como

Trabalhe com um exemplo numérico no papel antes de editar o starter: anote entradas, estado intermediário e saída esperada.

### Por quê

Sem o modelo mental no papel, o código vira tentativa-e-erro e os testes não ensinam o invariante.

### Por quê comparar com produção

Implementações reais (libc, kernels, VMs, GPUs) usam as mesmas ideias com mais camadas; este lab isola o núcleo.

### Por quê falhar de propósito no starter

O starter compila e o teste falha até o TODO existir — isso prova que o harness mede o comportamento certo.

### Trace manual

`	ext
entrada -> transformação -> invariante -> saída
` 

### Bugs comuns (módulo)

| Sintoma | Causa | Depuração |
|---------|-------|-----------|
| Teste falha após 'implementar' | Off-by-one / endian | Trace byte a byte |
| PASS sem entender | Copiou gabarito | Refaça o paper-trace |

