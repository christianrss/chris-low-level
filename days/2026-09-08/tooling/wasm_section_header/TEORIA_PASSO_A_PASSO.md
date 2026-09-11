# Teoria passo a passo — cabeçalho WASM em Assembly

Este laboratório é em **Assembly (MASM x64)**. Não é um esboço em Python com o mesmo nome.

## Por que este laboratório existe

O módulo de tooling deste dia não é um script. Você compara bytes de um módulo WASM na linguagem da máquina. No Windows o primeiro argumento chega em RCX (x64 ABI da Microsoft).

Por quê começar pelo formato, e não pela API da linguagem? Porque o bug clássico
aqui é **desalinhamento**: o programa “funciona” no exemplo errado e falha no
assert do teste com um número diferente do esperado.

## Contrato de dados

| Campo | Papel neste lab |
|-------|-------------|
| formato | ver a tabela abaixo |
| teste | compara o número do trace, não a intenção |

| Offset | Byte | Significado |
|--------|------|-----------|
| 0 | 00 | magic |
| 1 | 61 | 'a' |
| 2 | 73 | 's' |
| 3 | 6D | 'm' |
| 4..7 | 01 00 00 00 | version = 1 (u32 LE) |
| id | CL | 1 type, 2 import |

## Trace numérico (os mesmos valores do teste)

Siga no papel **antes** de abrir o editor. Os números abaixo são os do Caso 1,
não um espaço em branco para preencher depois.

```text
ponteiro RCX → 00 61 73 6D 01 00 00 00
[rcx+0]=00, +1=61, +2=73, +3=6D → eax=1
dword [rcx+4] = 1 (little-endian) → version ok
section_class(1) → eax=1
section_class(2) → eax=2
section_class(9) → eax=0
magic quebrado 00 61 73 00 → eax=0
```

## Algoritmo (ordem obrigatória)

1. Compare 4 bytes. Qualquer diferença zera EAX e ret.
2. Leia dword em RCX+4 e compare com 1.
3. section_class usa CL (byte baixo de RCX). 1 ou 2; senão 0.

## Invariantes

- A saída é determinística para a mesma entrada.
- Tamanho consumido e texto/valor produzido mudam juntos: se o tamanho estiver
  errado, o próximo byte é lido como opcode e o teste vê outra string.
- Erro de formato falha **agora** (retorno negativo, `Err`, `false`, exceção),
  não um valor default silencioso.

## Bugs que o teste rejeita

- Esquecer o byte 6D: magic `\0asm` incompleto passa no stub (eax=0) e o teste exige 1.
- Ler version em big-endian (byte 7): o 1 está no offset 4, não no 7.
- Tratar id 9 como type: o teste exige 0.

## Lab versus produção

wasm-objdump faz a mesma checagem de magic. Aqui são três predicados em Assembly para ver o ABI (RCX/EAX) sem runtime WASM.

## Checklist antes de compilar

- [ ] Escrevi no papel o valor esperado do Caso 1 (está na seção de trace).
- [ ] Sei qual arquivo e qual função recebem o corpo novo.
- [ ] Sei o que **não** mudar (assinatura, nomes dos opcodes, capacidade do buffer).

Por quê não pular o trace? O teste compara bytes, não a intenção.

## Mecanismo interno (segunda camada)

Neste módulo `tooling/wasm_section_header`, o fluxo de dados não é abstrato: cada função do starter
transforma um buffer ou um estado finito e devolve um valor que o teste compara
com igualdade estrita.

```text
entrada (fixture / literal do teste)
    → validação de limites (OOB / estado ilegal)
    → transformação (decode / fold / push / parse)
    → saída (string, código, ponteiro, probabilidade)
```

Por quê essa ordem? Se a validação vier depois da transformação, um buffer curto
gera leitura lixo e o assert falha com um número “quase certo”, difícil de depurar.

## Estruturas e papéis

| Peça | Papel | O que o teste fixa |
|------|-------|--------------------|
| buffer / stream | memória linear | bytes literais no caso |
| cursor / pc / head | progresso | avanço exatamente do size |
| estado / flags | FSM ou capacidade | transição ilegal rejeitada |
| retorno de erro | falha explícita | -1 / Err / false / throw |

## Trace estendido (mesmo caso, mais colunas)

Reescreva o Caso 1 da TEORIA com quatro colunas no papel:

```text
passo | cursor | lê | produz
------+--------+----+--------
(use os números já listados acima; não invente outro exemplo)
```

Se o cursor após o passo N não for o início do passo N+1, o listing ou o anel
desalinha e a string/valor diverge do assert.

## Invariantes reforçadas

1. Mesma entrada → mesma saída (determinismo).
2. Erro de formato não vira valor default silencioso.
3. Capacidade / size / transição ilegal falha **agora**.
4. O arquivo editado é só o citado na RESOLUCAO; o teste não se altera.

## Depuração dirigida

| Sintoma no teste | Hipótese #1 | O que imprimir |
|------------------|-------------|----------------|
| string/valor off-by-one | endianness ou size | hex do buffer e cursor |
| falha só no 2º caso | estado residual | reset entre casos |
| passe local, falha no runner | cwd / fixture path | path absoluto do fixture |

## Comparação com produção (detalhe)

Em ferramentas reais o mesmo contrato aparece com outros nomes: `objdump` (size
por opcode), `epoll` (anel de eventos), `softmax` em kernels CUDA (max-subtract).
Aqui o recorte é pequeno o bastante para caber no papel e grande o bastante para
o assert rejeitar o bug clássico.

## Trecho âncora do gabarito (só para conferir assinaturas)

Não copie cegamente. Use para confirmar nomes de funções e constantes:

```text
#ifndef WASM_API_H
#define WASM_API_H
int wasm_magic_ok(const unsigned char *p);
int wasm_version_is_1(const unsigned char *p);
int section_class(unsigned char id);
#endif
```

## Magic e versão (wire)

```text
offset 0: 00 61 73 6D   "\0asm"
offset 4: 01 00 00 00   version = 1 (u32 LE)
```

Calling convention Windows x64: ponteiro do buffer em **RCX**.
`wasm_magic_ok`: compara 4 bytes; EAX=1 sucesso, 0 falha.
`wasm_version_is_1`: `dword [RCX+4] == 1`.
`section_class`: CL=id → 1 (type), 2 (import), senão 0.
Id 9 → 0 (não é type/import).

Trace:

```text
buf = 00 61 73 6D 01 00 00 00
magic_ok → 1
version_is_1 → 1
section_class(1) → 1
section_class(2) → 2
section_class(9) → 0
```

**Por quê** Assembly? Para ver o ABI e o load byte-a-byte sem C
esconder o endian da dword.

## Invariantes

- Magic é 4 cmp separados (não um dword) — ordem de bytes explícita
- Version lê dword LE nativa
- section_class não lê memória, só CL

## Bugs comuns

- Comparar magic como dword 0x6D736100 no registrador errado
- Usar RDX em vez de RCX no Windows
- Devolver 1 para id desconhecido

## Lab vs produção

Wasmer/Wasmtime parseiam LEB128 de section size. Aqui só o
**header mínimo** + classificação de id.

## Checklist

- [ ] 4 bytes do magic no papel
- [ ] version dword = 1
- [ ] id 9 → 0
