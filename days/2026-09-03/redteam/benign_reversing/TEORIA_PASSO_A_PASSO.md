# Teoria passo a passo — Red Team / reversing benigno

## 1. Limite de segurança

Use somente `lab_target` deste pacote. Objetivo: entender binários, assembly e debugging — sem malware, persistência ou ataque a terceiros.

## 2. O que estamos construindo

- extrator ASCII de strings (`RE-STRINGS-01`);
- regra YARA educacional (`RE-YARA-01`);
- análise do alvo `verify_code` que transforma entrada byte a byte.

## 3. Pipeline estático → dinâmico

```text
fonte .c -> compilador -> PE/ELF
                |
                +--> strings ASCII (estático)
                +--> disassembly (objdump)
                +--> debugger (dinâmico)
                +--> YARA (assinatura)
```

## 4. Alvo benigno — lógica interna

```text
transformed[i] = (input[i] XOR 0x2A) + i
comparar com tabela constante
```

Exemplo manual com entrada `"A"` (0x41):

```text
(0x41 XOR 0x2A) + 0 = 0x6B
```

Índice `i` desloca cada byte — não é XOR simples.

## 5. Extrator ASCII — máquina de estados

```text
para cada byte b em data:
  se 0x20 <= b <= 0x7E:
    se start is None: start = index
  senão:
    se run >= min_len: salvar (start, run)
    start = None
```

Runs curtos que terminam no fim do buffer também devem ser capturados.

## 6. YARA educacional

Strings únicas do lab:

```text
LOWLEVEL-REVERSING-LAB-V1
accepted
rejected
```

Condição típica: `$marker and $accepted and $rejected`.

## 7. Calling conventions (referência)

| SO | 1º arg int | 2º arg int | retorno |
|----|------------|------------|---------|
| Linux System V | RDI | RSI | RAX |
| Windows x64 | RCX | RDX | RAX |

Debug sem símbolos exige inferir por convenção e padrões de código.

## 8. Invariantes

- Extrator só reporta bytes imprimíveis consecutivos ≥ `min_len`.
- YARA deve identificar exclusivamente o binário do lab (strings controladas).
- Pseudocódigo derivado do assembly deve bater com o fonte antes de consultar solução.

## 9. Complexidade

- Scan de strings: O(n) no tamanho do binário.
- `verify_code`: O(k) no tamanho da entrada.
- YARA match: O(n * p) no pior caso (n bytes, p padrões simples).

## 10. Bugs comuns

- Extrator não fecha run no EOF.
- Confundir offset de arquivo com RVA ao comparar com disassembly.
- YARA com strings genéricas (`"main"`) — falso positivo.
- Atribuir comportamento malicioso a strings inofensivas.
- Ignorar que Release otimiza e muda assembly vs Debug.

## 11. Comparação com produção

| Lab | Triagem real (SOC / IR) |
|-----|-------------------------|
| um binário conhecido | milhares de amostras/dia |
| strings manuais | YARA + sandbox + ML |
| debugger local | telemetria EDR |
| alvo benigno | malware isolado em VM air-gap |

Técnicas são as mesmas; escala e risco exigem processo.

## 12. Passo a passo guiado

1. Compile `lab_target` Debug e Release.
2. Rode `ascii_strings.py` no binário.
3. Disassemble e localize o loop de `verify_code`.
4. Debugger: breakpoint, argumentos, registradores.
5. Complete `lab_target.yar`.
6. Testes: `test_ascii_strings.py`, `test_rule.py`.

## 13. Como saber se está correto

Strings esperadas encontradas; regra YARA contém marcadores; testes Python passam.
## 4. Pipeline de análise benigna

```text
binário -> strings ASCII -> regra YARA -> relatório
```

## 5. Runs de strings

Byte imprimível (0x20-0x7E) estende run; <4 bytes descarta.

## 6. YARA didático

Strings `$a` únicas + condição `all of them` — sem shellcode real.

## 7. Ética e escopo

Somente binários do laboratório. Não distribuir regras contra software de terceiros.

## 8. Invariantes

- Offsets reportados em decimal ou hex consistente.
- Runs não cruzam seções não mapeadas (aqui: arquivo inteiro).

## 9. Bugs comuns

- Confundir UTF-16 LE com ASCII.
- Regra YARA ampla demais (falsos positivos).

---

## Por quê — síntese pedagógica

### Por quê este módulo existe?
Conectar teoria de baixo nível a decisões de implementação verificáveis — não decorar API.

### Por quê estas invariantes?
Cada `TODO [ID]` protege uma propriedade que quebra silenciosamente em produção se ignorada (overflow, estado inválido, parsing parcial).

### Por quê medir e portar para `projects/`?
Lab isola o aprendizado; `projects/chris-*` consolida engenharia de portfólio com testes e benchmarks reproduzíveis.
