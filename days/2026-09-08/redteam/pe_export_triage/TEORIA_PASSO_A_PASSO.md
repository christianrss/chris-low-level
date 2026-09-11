# Teoria passo a passo — triage de export PE

Este laboratório é em **Python**. Não é um esboço em Python com o mesmo nome.

## Por que este laboratório existe

O lab .NET lê o RVA 0x1000. Este Python (red team do dia) só decide se o buffer é PE e se um nome de export é suspeito. Não executa o binário.

Por quê começar pelo formato, e não pela API da linguagem? Porque o bug clássico
aqui é **desalinhamento**: o programa “funciona” no exemplo errado e falha no
assert do teste com um número diferente do esperado.

## Contrato de dados

| Campo | Papel neste lab |
|-------|-------------|
| formato | ver a tabela abaixo |
| teste | compara o número do trace, não a intenção |

| Offset | Campo no teste | Valor |
|--------|----------------|-------|
| 0 | MZ | `4D 5A` |
| 0x3C | e_lfanew | 0x80 |
| 0x80 | PE | `PE` |
| nomes | VirtualAlloc, malloc | só o primeiro é suspeito |

## Trace numérico (os mesmos valores do teste)

Siga no papel **antes** de abrir o editor. Os números abaixo são os do Caso 1,
não um espaço em branco para preencher depois.

```text
minimal_pe: 0x100 bytes, MZ, e_lfanew=0x80, PE em 0x80
validate_mz_pe(pe) == True
count_export_names(pe, ["A", "B"]) == 2
flag_suspicious_exports(["VirtualAlloc", "malloc"]) == ["VirtualAlloc"]
count_export_names(b"bad", []) == -1
```

## Algoritmo (ordem obrigatória)

1. MZ e PE via e_lfanew little-endian em 0x3C.
2. Se PE inválido, count retorna -1. Senão len(names).
3. Filtre nomes que estão na tupla SUSPICIOUS.

## Invariantes

- A saída é determinística para a mesma entrada.
- Tamanho consumido e texto/valor produzido mudam juntos: se o tamanho estiver
  errado, o próximo byte é lido como opcode e o teste vê outra string.
- Erro de formato falha **agora** (retorno negativo, `Err`, `false`, exceção),
  não um valor default silencioso.

## Bugs que o teste rejeita

- Tratar `b"bad"` como PE: count deve ser -1.
- Incluir malloc na lista suspeita: o teste espera só VirtualAlloc.

## Lab versus produção

O parser de RVA está no lab C#. Este script é a camada de evidência que o analista roda sem o SDK.

## Checklist antes de compilar

- [ ] Escrevi no papel o valor esperado do Caso 1 (está na seção de trace).
- [ ] Sei qual arquivo e qual função recebem o corpo novo.
- [ ] Sei o que **não** mudar (assinatura, nomes dos opcodes, capacidade do buffer).

Por quê não pular o trace? O teste compara bytes, não a intenção.

## Mecanismo interno (segunda camada)

Neste módulo `redteam/pe_export_triage`, o fluxo de dados não é abstrato: cada função do starter
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
"""PE export table triage — validate MZ/PE and flag suspicious names."""

from __future__ import annotations

SUSPICIOUS = ("VirtualAlloc", "WriteProcessMemory", "CreateRemoteThread")


def validate_mz_pe(data: bytes) -> bool:
    # PEDAGOGY-SOLUTION: RT-PE-EXP-01
    if len(data) < 0x40 or data[0:2] != b"MZ":
        return False
    import struct
    pe_off = struct.unpack_from("<I", data, 0x3C)[0]
    return pe_off + 4 <= len(data) and data[pe_off:pe_off + 2] == b"PE"


def count_export_names(data: bytes, names: list[str]) -> int:
    # PEDAGOGY-SOLUTION: RT-PE-EXP-02
    if not validate_mz_pe(data):
        return -1
    return len(names)


def flag_suspicious_exports(names: list[str]) -> list[str]:
    # PEDAGOGY-SOLUTION: RT-PE-EXP-03
    return [n for n in names if n in SUSPICIOUS]
```

## Pipeline de triage

```text
bytes → validate_mz_pe → count_export_names → flag_suspicious_exports
```

`SUSPICIOUS = VirtualAlloc, WriteProcessMemory, CreateRemoteThread`
(clássico de injection).

Trace:

```text
data com MZ + PE → validate True
names=["VirtualAlloc","foo"] → flagged=["VirtualAlloc"]
data sem MZ → validate False; count retorna -1
```

**Por quê** Python aqui? Triage rápida de evidência sem Span/.NET —
par com `dotnet/pe_export_span` no mesmo dia (mesmos offsets 0x3C / PE).

## Wire (igual .NET)

```text
0x00 MZ
0x3C e_lfanew u32 LE
[e_lfanew] PE\0\0
```

## Invariantes

- Sem MZ/PE válido, `count_export_names` = -1
- Flag é filtro por nome exato (não substring)
- Não resolve RVA→nomes neste lab (nomes vêm da lista de teste)

## Bugs comuns

- `data.startswith("MZ")` em str em vez de bytes
- Endian errado em `struct.unpack_from("<I", ...)`
- Flag case-insensitive demais / de menos

## Lab vs produção

Ferramentas reais (pefile, capa) enumeram Export Address Table.
Aqui o foco é **heurística de nomes** depois da validação de header.

## Checklist

- [ ] MZ nos 2 primeiros bytes
- [ ] PE em e_lfanew
- [ ] VirtualAlloc entra na lista suspeita
