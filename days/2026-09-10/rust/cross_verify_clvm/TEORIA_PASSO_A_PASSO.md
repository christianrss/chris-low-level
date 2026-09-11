# Teoria passo a passo — Cross-verify header CLVM (Rust)

Este laboratório é em **Rust**.

## 1. O que estamos construindo

Valida magic `CLVM`, version 1 e FNV no offset 12 — o mesmo contrato do loader C, em Rust memory-safe.

## 2. Por que este módulo existe neste dia

Por quê estudar isso agora? Porque o contrato numérico do teste fixa o vocabulário
do resto do dia — sem o paper-trace, o código “quase certo” passa no olho e falha
no assert.

## 3. Formato / contrato de dados (wire)

| Offset | Campo |
|--------|-------|
| 0 | magic `CLVM` |
| 4 | version = 1 |
| 12 | checksum FNV-1a do bytecode |

FNV: offset 0x811C9DC5, prime 16777619.

## 4. Trace numérico (valores dos testes)

Siga no papel **antes** de abrir o editor. Estes números são os do Caso 1.

```text
header válido → Ok
magic errado → Err
checksum != FNV(payload) → Err
```

## 5. Algoritmo (ordem obrigatória)

1. leia magic/version.
2. calcule FNV do code.
3. compare com u32 LE @12.

## 6. Invariantes

- A saída é determinística para a mesma entrada do teste.
- Erros de pré-condição falham **agora** (retorno negativo, `Err`, `false`, exceção),
  não um default silencioso.
- O valor que o assert compara é o da seção de trace — não um sinônimo.

## 7. Bugs que o teste rejeita

- FNV sem mask 32-bit.
- version != 1 aceito.
- endianness do checksum.

## 8. Lab versus produção

Mesmo padrão do rust-validator Dia 03.

## Modelo mental

bytes → Result<(), E> sem executar.

## Por quê FNV?

Checksum toy alinhado ao CLVM do curso.

## Por quê Rust no capstone?

Cross-check do loader C/Python.

## Invariante

Ok só se magic+version+FNV batem.

## Ligação

clvm_pipeline_integration executa; este só verifica.

## Teste

cargo test integration.


## Por quê — síntese

### Por quê estas invariantes?
Cada `TODO [ID]` isola uma propriedade que quebra silenciosamente se ignorada.

### Por quê medir?
O `BENCHMARK_GUIADO.md` pede a métrica `1e5 validates` — mesmo que o ambiente
pule a medição, o aluno registra o protocolo.

### Por quê não alterar o teste?
O teste é o contrato. Ajuste o código até a saída igualar o caderno.

## Checklist antes de implementar

- [ ] Escrevi no papel o valor do Caso 1 (seção 4).
- [ ] Sei arquivo/função de cada TODO (`RESOLUCAO` / `TODO_MAP`).
- [ ] Sei o que **não** mudar (assinaturas, nomes públicos, capacidade fixa).

## Como saber se está correto

Rode os testes do `starter/` (esperado FAIL) e depois os de `solutions/` (PASS).
A string/número impresso deve bater com o trace caractere a caractere / bit a bit.

## Fluxo de dados (visão única deste módulo)

```text
entrada do Caso 1  →  transformação do algoritmo (seção 5)  →  valor do assert
       ↑                          ↑                                ↑
  paper-trace              código no starter                  TESTES_GUIADOS
```

Se qualquer seta divergir, pare: o bug está na seta, não no “conceito geral”.

## Tabela rápida TODO → propriedade

| Ordem | Propriedade protegida |
|-------|------------------------|
| 1º TODO | base do contrato (parse/init/open) |
| 2º TODO | transformação / estado intermediário |
| 3º TODO | agregação / export / verificação final |

Substitua na ordem da RESOLUCAO: pular o 1º faz o 2º mentir com dados lixo.

## O que não fazer

- Não reescrever o módulo em outra linguagem “porque é mais fácil”.
- Não alterar asserts para caber na sua saída.
- Não inventar um segundo exemplo no lugar do trace do Caso 1.
- Não copiar `solutions/` no começo — use a RESOLUCAO só ao travar.

## Fechamento

Releia o wire (seção 3) e o trace (seção 4). Risque no caderno a linha que você
calculou diferente do teste. Só então abra o arquivo do starter citado na
resolução e substitua o corpo da função nomeada.

## Mecanismo interno (segunda camada)

Neste módulo `rust/cross_verify_clvm`, o fluxo de dados não é abstrato: cada função do starter
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
//! Cross-verify CLVM bytecode with Python reference (FNV checksum).

pub const MAGIC: &[u8; 4] = b"CLVM";

pub fn fnv1a32(data: &[u8]) -> u32 {
    let mut h = 0x811C_9DC5u32;
    for &b in data {
        h ^= u32::from(b);
        h = h.wrapping_mul(0x0100_0193);
    }
    h
}

/// PEDAGOGY-SOLUTION: CAP-RS-XVFY-01
pub fn validate_header(data: &[u8]) -> bool {
    data.len() >= 16 && data.starts_with(MAGIC) && data[4] == 1
}

/// PEDAGOGY-SOLUTION: CAP-RS-XVFY-02
pub fn extract_code(data: &[u8]) -> Option<Vec<u8>> {
    if data.len() < 16 { return None; }
    let size = u32::from_le_bytes(data[8..12].try_into().unwrap()) as usize;
    if data.len() < 16 + size { return None; }
    Some(data[16..16+size].to_vec())
}

/// PEDAGOGY-SOLUTION: CAP-RS-XVFY-03
pub fn verify_checksum(data: &[u8]) -> bool {
    let code = match extract_code(data) {
        Some(c) => c,
        None => return false,
    };
    let expected = u32::from_le_bytes(data[12..16].try_into().unwrap());
    fnv1a32(&code) == expected
}
```

## Fechamento teórico

Antes de abrir o editor: (1) valor do Caso 1 no papel; (2) arquivo + função;
(3) o que **não** mudar. Por quê essa trava? Porque “compilar até passar”
sem o número no papel produz soluções que quebram no próximo fixture.
