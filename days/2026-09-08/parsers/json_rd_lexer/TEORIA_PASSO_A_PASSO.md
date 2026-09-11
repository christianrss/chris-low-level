# Teoria passo a passo — lexer JSON em C

Este laboratório é em **C**. Não é um esboço em Python com o mesmo nome.

## Por que este laboratório existe

O Pratt do Dia 07 assume tokens prontos. Aqui você produz os tokens de um subset JSON: chaves, string sem escape, número decimal sem sinal, vírgula e dois-pontos.

Por quê começar pelo formato, e não pela API da linguagem? Porque o bug clássico
aqui é **desalinhamento**: o programa “funciona” no exemplo errado e falha no
assert do teste com um número diferente do esperado.

## Contrato de dados

| Campo | Papel neste lab |
|-------|-------------|
| formato | ver a tabela abaixo |
| teste | compara o número do trace, não a intenção |

| Lexema | kind | end-start |
|--------|------|-----------|
| `{` | 1 LBRACE | 1 |
| `42` | 3 NUMBER | 2 |
| `"ab"` | 4 STRING | 4 (aspas inclusas) |
| objeto `{"a":1}` | 5 tokens | `{` `"a"` `:` `1` `}` |

## Trace numérico (os mesmos valores do teste)

Siga no papel **antes** de abrir o editor. Os números abaixo são os do Caso 1,
não um espaço em branco para preencher depois.

```text
skip_ws("  {", 0) → índice 2 (dois espaços)
next "{": kind=1, consome 1, cursor=1
next "42": kind=3, start=0, end=2 (não inclui lixo depois)
"ab" : aspas, 'a','b', aspas → end=4
{"a":1} tokens:
  1 {   2 "a"   3 :   4 1   5 }
lex_count == 5
```

## Algoritmo (ordem obrigatória)

1. skip_ws avança espaço, tab e newline.
2. next_token classifica um lexema e devolve o índice seguinte.
3. String: do `"` de abertura até o fechamento, sem escapes neste lab.
4. Número: dígitos ASCII '0'..'9' apenas.
5. lex_count chama next_token até o fim e conta os que não são END.

## Invariantes

- A saída é determinística para a mesma entrada.
- Tamanho consumido e texto/valor produzido mudam juntos: se o tamanho estiver
  errado, o próximo byte é lido como opcode e o teste vê outra string.
- Erro de formato falha **agora** (retorno negativo, `Err`, `false`, exceção),
  não um valor default silencioso.

## Bugs que o teste rejeita

- Contar `{"a":1}` como 3 (esquecer `:` e número): o teste exige 5.
- String sem as aspas de fechamento: retorno -1.
- skip_ws não avançar: next_token de `"  {"` no índice 0 não vê a chave.

## Lab versus produção

O lexer de produção (jq, simdjson) trata escapes e unicode. Este subset é o mínimo para ver o cursor `i` avançar.

## Checklist antes de compilar

- [ ] Escrevi no papel o valor esperado do Caso 1 (está na seção de trace).
- [ ] Sei qual arquivo e qual função recebem o corpo novo.
- [ ] Sei o que **não** mudar (assinatura, nomes dos opcodes, capacidade do buffer).

Por quê não pular o trace? O teste compara bytes, não a intenção.

## Mecanismo interno (segunda camada)

Neste módulo `parsers/json_rd_lexer`, o fluxo de dados não é abstrato: cada função do starter
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
#ifdef __cplusplus
# error "A C++ compiler has been selected for C."
#endif

#if defined(__18CXX)
# define ID_VOID_MAIN
#endif
#if defined(__CLASSIC_C__)
/* cv-qualifiers did not exist in K&R C */
# define const
# define volatile
#endif

#if !defined(__has_include)
/* If the compiler does not have __has_include, pretend the answer is
   always no.  */
#  define __has_include(x) 0
#endif


/* Version number components: V=Version, R=Revision, P=Patch
   Version date components:   YYYY=Year, MM=Month,   DD=Day  */

#if defined(__INTEL_COMPILER) || defined(__ICC)
# define COMPILER_ID "Intel"
# if defined(_MSC_VER)
#  define SIMULATE_ID "MSVC"
# endif
# if defined(__GNUC__)
#  define SIMULATE_ID "GNU"
# endif
  /* __INTEL_COMPILER = VRP prior to 2021, and then VVVV for 2021 and later,
     except that a few beta releases use the old format with V=2021.  */
# if __INTEL_COMPILER < 2021 || __INTEL_COMPILER == 202110 || __INTEL_COMPILER == 202111
#  define COMPILER_VERSION_MAJOR DEC(__INTEL_COMPILER/100)
#  define COMPILER_VERSION_MINOR DEC(__INTEL_COMPILER/10 % 10)
#  if defined(__INTEL_COMPILER_UPDATE)
#   define COMPILER_VERSION_PATCH DEC(__INTEL_COMPILER_UPDATE)
#  else
#   define COMPILER_VERSION_PATCH DEC(__INTEL_COMPILER   % 10)
```

## Tokens do subset

| Char / padrão | kind |
|---------------|------|
| `{` | TOK_LBRACE |
| `}` | TOK_RBRACE |
| `:` | TOK_COLON |
| `,` | TOK_COMMA |
| `"..."` | TOK_STRING |
| `[0-9]+` | TOK_NUMBER |
| EOF | TOK_END |

Trace `{"a":1}`:

```text
i=0 '{' → LBRACE, i=1
i=1 '"'…'"' → STRING "a", i=4
i=4 ':' → COLON, i=5
i=5 '1' → NUMBER, i=6
i=6 '}' → RBRACE, i=7
lex_count = 5
```

**Por quê** lexer antes do parser? O recursive-descent (nome do módulo)
come tokens, não caracteres — whitespace some em `skip_ws`.

## Invariantes

- `skip_ws` só come espaço, `\n`, `\t`
- String sem `"` final → -1
- `lex_count` não conta TOK_END

## Bugs comuns

- Contar whitespace como token
- Aceitar letras em NUMBER
- Off-by-one em `end` da string

## Lab vs produção

`serde_json` / `simdjson` têm escapes e Unicode. Aqui o subset é
ASCII mínimo — suficiente para sentir o cursor `i`.

## Checklist

- [ ] `{"a":1}` → 5 tokens
- [ ] skip_ws em `"  {"` aponta para `{`
- [ ] string aberta falha
