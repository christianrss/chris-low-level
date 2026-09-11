# Teoria passo a passo — disassembler CLVM em Rust

Este laboratório é em **Rust**. Não é um esboço em Python com o mesmo nome.

## Por que este laboratório existe

Par do disassembler C do mesmo dia. A ISA é a mesma; o tipo de erro é `Result`, não um int -1.

Por quê começar pelo formato, e não pela API da linguagem? Porque o bug clássico
aqui é **desalinhamento**: o programa “funciona” no exemplo errado e falha no
assert do teste com um número diferente do esperado.

## Contrato de dados

| Campo | Papel neste lab |
|-------|-------------|
| formato | ver a tabela abaixo |
| teste | compara o número do trace, não a intenção |

| Função | Contrato |
|--------|----------|
| `opcode_name(0x01)` | `Some("PUSH")` |
| `opcode_name(0x08)` | `Some("HALT")` |
| `instruction_size(0x01)` | 5 |
| `instruction_size(0x09)` | 3 |
| `disassemble([01,42,0,0,0,08])` | `["PUSH 42", "HALT"]` |

## Trace numérico (os mesmos valores do teste)

Siga no papel **antes** de abrir o editor. Os números abaixo são os do Caso 1,
não um espaço em branco para preencher depois.

```text
opcode 0x01 → Some("PUSH")
opcode 0x08 → Some("HALT")
size(PUSH)=5, size(JMP=0x09)=3, size(HALT)=1
bytes [01, 2A, 00, 00, 00, 08]
  pc=0 PUSH imm=42, avança 5
  pc=5 HALT, avança 1
  ["PUSH 42", "HALT"]
[FF] → Err
```

## Algoritmo (ordem obrigatória)

1. Nomeie PUSH/ADD/HALT/JMP.
2. Tamanho: PUSH 5, branch 3, resto 1.
3. Walk com `from_le_bytes` no imediato.

## Invariantes

- A saída é determinística para a mesma entrada.
- Tamanho consumido e texto/valor produzido mudam juntos: se o tamanho estiver
  errado, o próximo byte é lido como opcode e o teste vê outra string.
- Erro de formato falha **agora** (retorno negativo, `Err`, `false`, exceção),
  não um valor default silencioso.

## Bugs que o teste rejeita

- size(PUSH)=1 quebra o disassemble (o 42 vira opcode).
- `None` para HALT falha o Caso 1.

## Lab versus produção

O crate Rust do Dia 07 (`clvm_v2_verify`) valida. Este lista.

## Checklist antes de compilar

- [ ] Escrevi no papel o valor esperado do Caso 1 (está na seção de trace).
- [ ] Sei qual arquivo e qual função recebem o corpo novo.
- [ ] Sei o que **não** mudar (assinatura, nomes dos opcodes, capacidade do buffer).

Por quê não pular o trace? O teste compara bytes, não a intenção.

## Mecanismo interno (segunda camada)

Neste módulo `rust/clvm_disasm`, o fluxo de dados não é abstrato: cada função do starter
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
//! CLVM bytecode disassembler — Rust port.

pub const PUSH: u8 = 0x01;

pub fn opcode_name(op: u8) -> Option<&'static str> {
    // PEDAGOGY-SOLUTION: CLVM-RS-DIS-01
    match op {
        0x02 => Some("ADD"),
        0x08 => Some("HALT"),
        0x09 => Some("JMP"),
        PUSH => Some("PUSH"),
        _ => None,
    }
}

pub fn instruction_size(op: u8) -> usize {
    // PEDAGOGY-SOLUTION: CLVM-RS-DIS-02
    if op == PUSH {
        5
    } else if matches!(op, 0x09 | 0x0A | 0x0B | 0x13) {
        3
    } else {
        1
    }
}

pub fn disassemble(code: &[u8]) -> Result<Vec<String>, String> {
    // PEDAGOGY-SOLUTION: CLVM-RS-DIS-03
    let mut out = Vec::new();
    let mut pc = 0usize;
    while pc < code.len() {
        let op = code[pc];
        if op == PUSH {
            if pc + 5 > code.len() {
                return Err("truncated PUSH".into());
            }
            let imm = u32::from_le_bytes(code[pc + 1..pc + 5].try_into().unwrap());
            out.push(format!("PUSH {}", imm));
            pc += 5;
        } else if matches!(op, 0x09 | 0x0A | 0x0B | 0x13) {
```

## Mesma ISA, superfície Rust

O C (`clvm_disassembler`) devolve `-1` / `snprintf`.
O Rust devolve `Result<Vec<String>, String>` e usa `u32::from_le_bytes`.

| Conceito | C | Rust |
|----------|---|------|
| falha | return -1 | `Err("truncated PUSH")` |
| imm32 | shifts manuais | `from_le_bytes` |
| walk | `pc += size` | idem em `while pc < len` |

## Trace idêntico ao C

```text
code = [0x01, 0x2A, 0x00, 0x00, 0x00, 0x08]
disassemble → Ok(["PUSH 42", "HALT"])
instruction_size(0x01) = 5
instruction_size(0x09) = 3
instruction_size(0x02) = 1
opcode_name(0xFF) = None
```

**Por quê** portar? Ownership e `Result` tornam o trust-boundary explícito:
bytes truncados não viram UB silenciosa.

## `instruction_size` antes do decode

Separar size do format permite um verifier futuro andar sem alocar strings.
O lab testa size isolado (`CLVM-RS-DIS-02`) antes do walk completo.

## Invariantes

- `Ok(lines)` ⇒ concat(sizes) == code.len()
- Opcode desconhecido ⇒ `Err`, não `"???"`
- PUSH truncado (len<5) ⇒ `Err("truncated PUSH")`

## Bugs comuns

- Usar `u32::from_be_bytes` → 704643072 em vez de 42
- Size PUSH=1 → listing desalinhado
- `unwrap` em slice curto → panic (o lab prefere `Err`)

## Lab vs produção

`capstone` / `iced-x86` geram tabelas; aqui a tabela cabe em um `match`.
O ethos é o mesmo do validador Rust do Dia 03/06: bounds antes de indexar.

## Checklist

- [ ] size(PUSH)=5, size(JMP)=3
- [ ] listing PUSH 42 / HALT
- [ ] unknown op → Err
