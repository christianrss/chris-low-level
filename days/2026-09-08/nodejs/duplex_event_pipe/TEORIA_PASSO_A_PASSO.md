# Teoria passo a passo — Duplex de eventos de 24 bytes

Este laboratório é em **JavaScript**. Não é um esboço em Python com o mesmo nome.

## Por que este laboratório existe

O Transform do Dia 07 só lê. Um Duplex escreve e lê o mesmo registro evdev de 24 bytes, com buffer parcial entre writes.

Por quê começar pelo formato, e não pela API da linguagem? Porque o bug clássico
aqui é **desalinhamento**: o programa “funciona” no exemplo errado e falha no
assert do teste com um número diferente do esperado.

## Contrato de dados

| Campo | Papel neste lab |
|-------|-------------|
| formato | ver a tabela abaixo |
| teste | compara o número do trace, não a intenção |

| Constante | Valor |
|-----------|-------|
| EVENT_SIZE | 24 |
| write de 48 bytes | 2 eventos |
| preenchimento do teste | byte 7 |
| metrics | eventsWritten, eventsRead |

## Trace numérico (os mesmos valores do teste)

Siga no papel **antes** de abrir o editor. Os números abaixo são os do Caso 1,
não um espaço em branco para preencher depois.

```text
ev = 24 bytes 0x07
write(ev+ev) = 48 bytes
_write corta em 24:
  eventsWritten=2
  cada fatia vai para _readBuf
_read empurra objetos de 24
metrics.eventsWritten === 2
write de 10 bytes não completa evento (fica no _writeBuf)
```

## Algoritmo (ordem obrigatória)

1. `_write` concatena e enquanto length>=24 emite para o buffer de leitura.
2. `_read` dá push de fatias de 24.
3. metrics devolve os dois contadores.

## Invariantes

- A saída é determinística para a mesma entrada.
- Tamanho consumido e texto/valor produzido mudam juntos: se o tamanho estiver
  errado, o próximo byte é lido como opcode e o teste vê outra string.
- Erro de formato falha **agora** (retorno negativo, `Err`, `false`, exceção),
  não um valor default silencioso.

## Bugs que o teste rejeita

- Cortar em 16: eventsWritten não é 2.
- Esquecer evento parcial: o 25º byte vaza como evento curto.

## Lab versus produção

Node Duplex é a base de `net.Socket`. Aqui o framing é fixo (24), como o struct do Dia 07.

## Checklist antes de compilar

- [ ] Escrevi no papel o valor esperado do Caso 1 (está na seção de trace).
- [ ] Sei qual arquivo e qual função recebem o corpo novo.
- [ ] Sei o que **não** mudar (assinatura, nomes dos opcodes, capacidade do buffer).

Por quê não pular o trace? O teste compara bytes, não a intenção.

## Mecanismo interno (segunda camada)

Neste módulo `nodejs/duplex_event_pipe`, o fluxo de dados não é abstrato: cada função do starter
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
import { Duplex } from "node:stream";

export const EVENT_SIZE = 24;

export class DuplexEventPipe extends Duplex {
    constructor() {
        super();
        this._writeBuf = Buffer.alloc(0);
        this._readBuf = Buffer.alloc(0);
        this.eventsWritten = 0;
        this.eventsRead = 0;
    }

    _write(chunk, encoding, callback) {
        // PEDAGOGY-SOLUTION: ND-DUPLEX-01
        this._writeBuf = Buffer.concat([this._writeBuf, chunk]);
        while (this._writeBuf.length >= EVENT_SIZE) {
            const ev = this._writeBuf.subarray(0, EVENT_SIZE);
            this._writeBuf = this._writeBuf.subarray(EVENT_SIZE);
            this._readBuf = Buffer.concat([this._readBuf, ev]);
            this.eventsWritten++;
        }
        this._read(EVENT_SIZE);
        callback();
    }

    _read(size) {
        // PEDAGOGY-SOLUTION: ND-DUPLEX-02
        while (this._readBuf.length >= EVENT_SIZE) {
            const ev = this._readBuf.subarray(0, EVENT_SIZE);
            this._readBuf = this._readBuf.subarray(EVENT_SIZE);
            this.eventsRead++;
            if (!this.push(ev)) break;
        }
    }

    metrics() {
        // PEDAGOGY-SOLUTION: ND-DUPLEX-03
        return { eventsWritten: this.eventsWritten, eventsRead: this.eventsRead };
    }
```

## Framing de 24 bytes

```text
EVENT_SIZE = 24
write 48 bytes → 2 eventos completos; eventsWritten == 2
write 25 bytes → 1 evento + 1 byte residual no _writeBuf
```

Fluxo:

```text
_write: concat → while len>=24: corta ev → _readBuf; eventsWritten++
_read:  while len>=24: push(ev); eventsRead++; respeita backpressure
metrics: {eventsWritten, eventsRead}
```

**Por quê** Duplex? Mesmo stream carrega input e output — padrão Node
para pipes binários (compare com Transform gunzip do Dia 06).

## Invariantes

- Só múltiplos de 24 sobem para o peer
- Residual < 24 permanece no buffer
- `push` false → para o loop (backpressure)

## Bugs comuns

- Usar `chunk.length` sem concat de residual
- Contar bytes em vez de eventos
- Ignorar retorno de `push`

## Lab vs produção

`objectMode` evita framing manual; aqui o framing ensina o bug clássico
de “meia mensagem”.

## Checklist

- [ ] 48 bytes → 2 eventos
- [ ] 25 bytes → 1 evento + residual 1
- [ ] metrics reflete contadores
