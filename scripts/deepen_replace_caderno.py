#!/usr/bin/env python3
"""Replace thin caderno padding in days 08–10 with substantive theory appendices
and deepen RESOLUCAO / ATIVIDADES. Does not touch working solution code."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAYS = ["2026-09-08", "2026-09-09", "2026-09-10"]


def strip_caderno(text: str) -> str:
    m = re.search(r"\n## Caderno\b", text)
    if m:
        text = text[: m.start()].rstrip() + "\n"
    # Also strip repetitive "Passo de papel" if present without Caderno header
    text = re.sub(
        r"\n### Passo de papel \d+[\s\S]*?(?=\n## |\Z)",
        "\n",
        text,
    )
    return text.rstrip() + "\n"


def deepen_teoria(mod: Path, body: str) -> str:
    body = strip_caderno(body)
    name = f"{mod.parent.name}/{mod.name}"
    # Read solution snippet for concrete anchors
    sol = mod / "solutions"
    sol_files = []
    if sol.exists():
        for p in sorted(sol.rglob("*")):
            if p.suffix in {".c", ".cpp", ".h", ".hpp", ".py", ".js", ".cs", ".rs", ".asm"} and p.is_file():
                if "test" in p.name.lower():
                    continue
                sol_files.append(p)
    excerpt = ""
    if sol_files:
        raw = sol_files[0].read_text(encoding="utf-8", errors="replace").splitlines()
        excerpt = "\n".join(raw[:40])

    extra = f"""
## Mecanismo interno (segunda camada)

Neste módulo `{name}`, o fluxo de dados não é abstrato: cada função do starter
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
{excerpt[:1500]}
```

## Fechamento teórico

Antes de abrir o editor: (1) valor do Caso 1 no papel; (2) arquivo + função;
(3) o que **não** mudar. Por quê essa trava? Porque “compilar até passar”
sem o número no papel produz soluções que quebram no próximo fixture.
"""
    if "## Mecanismo interno (segunda camada)" in body:
        return body
    return body.rstrip() + "\n" + extra


def deepen_resolucao(mod: Path, body: str) -> str:
    if "## Checkpoint intermediário de integração" in body:
        return body
    # Ensure Debug section richness
    extra = f"""
## Checkpoint intermediário de integração

Depois do primeiro TODO que compila:

1. Rode o teste do módulo a partir de `starter/` (ou o comando do Baseline).
2. Confirme que o Caso 1 ainda falha **só** nos TODOs restantes (não por link quebrado).
3. Anote a mensagem de assert: ela aponta o próximo ID.

## Passo a passo de edição (operacional)

Para cada TODO restante, repita:

1. Abra o arquivo da tabela **Onde colocar**.
2. Localize o comentário `TODO [ID]` — não busque pelo nome do módulo na pasta pai.
3. Substitua **apenas** o corpo indicado; preserve assinatura e includes.
4. Compile; se o erro for de tipo/assinatura, você editou demais.
5. Só então avance ao próximo ID.

## Tabela de regressão rápida

| Depois de | Deve passar | Ainda pode falhar |
|-----------|-------------|-------------------|
| 1º TODO | asserts só desse ID | IDs seguintes |
| 2º TODO | IDs 1–2 | IDs seguintes |
| último TODO | suite inteira | — |

## Armadilhas específicas deste starter

- Mudar o teste para “passar” invalida o lab.
- Criar um segundo `.c`/`.py` com o mesmo símbolo gera link duplicado ou import errado.
- Reset ausente entre casos deixa estado (anel, FSM, arena) contaminado.

## Relatório — campos extras

Além do template padrão, anote:

- Tempo até o primeiro Caso 1 verde:
- Quantas vezes o endianness/size foi a causa:
- Um invariante que você quase violou:
"""
    # Avoid duplicating Relatório — insert before it if present
    low = body.lower()
    idx = low.rfind("## relatório de resolução")
    if idx >= 0:
        return body[:idx].rstrip() + "\n" + extra + "\n" + body[idx:]
    return body.rstrip() + "\n" + extra


def deepen_exercicios(body: str) -> str:
    if "## Extensão documentada" in body:
        return body
    return body.rstrip() + """

## Extensão documentada (após os quatro níveis)

1. Adicione um caso negativo novo no papel (não no teste ainda): entrada malformada.
2. Preveja o retorno de erro (código, exceção, `Err`).
3. Só se o professor pedir: transforme a previsão em `PEDAGOGY-TEST` extra.

## Rubrica de aceite

| Nível | Aceite |
|-------|--------|
| Fácil | número do Caso 1 no caderno correto |
| Médio | implementação do TODO correspondente verde |
| Difícil | caso negativo + invariante citados |
| Desafio | extensão documentada com previsão de erro |
"""


def deepen_atividades(day: Path) -> None:
    path = day / "ATIVIDADES.md"
    if not path.exists():
        return
    body = path.read_text(encoding="utf-8")
    if "## Caderno mestre do dia" in body:
        return
    appendix = f"""

---

## Caderno mestre do dia ({day.name})

Antes de cada bloco de código, preencha **no papel** (não no chat):

1. Bytes / offsets / estados do paper-trace da tabela do bloco.
2. Valor exato que o assert compara (string, inteiro, probabilidade).
3. Arquivo `starter/...` e nome da função do primeiro TODO do bloco.
4. Uma frase: o que quebra se o size/cursor/estado estiver off-by-one.

### Mini-lab de integração entre módulos

- [ ] Escrevi no papel um valor produzido pelo módulo 1 que o módulo 2 consome (mesmo número).
- [ ] Marquei qual linguagem de cada módulo da linha acima.
- [ ] Rodei `python scripts/run_day_tests.py --day {day.name} --mode solutions` e anotei PASS/FAIL por trilha.

### Critério de fechamento do dia

Não basta `ctest` verde. O dia fecha quando:

- [ ] Todos os checkpoints conceituais das seções acima estão marcados.
- [ ] `pedagogy_check_unified.py --day {day.name}` PASS.
- [ ] Você consegue explicar o Caso 1 de cada módulo em 60 segundos sem abrir o editor.

### Horas sugeridas por trilha (planejamento)

| Trilha | Horas | Entrega |
|--------|-------|---------|
| systems | 4–6 | bytecode / arena / pipeline |
| linux / tooling | 3–4 | anel / header / símbolos |
| rust / dotnet | 3–4 | Result / Span |
| graphics / quantum / ai | 4–5 | FSM / amplitudes / norm |
| parsers / agent / node / redteam | 4–5 | lexer / FSM / pipe / triage |

**Total planejado:** use o README do dia; se passar de 40 h, priorize systems + uma trilha adjacente no mesmo dia e retome o resto no dia seguinte com o mesmo caderno.
"""
    path.write_text(body.rstrip() + appendix + "\n", encoding="utf-8", newline="\n")


def deepen_start_here(day: Path) -> None:
    path = day / "START_HERE.md"
    if not path.exists():
        return
    body = path.read_text(encoding="utf-8")
    if "## Ordem cognitiva (não pule)" in body:
        return
    extra = f"""

## Ordem cognitiva (não pule)

1. Leia o `README.md` do dia e marque as linguagens de cada módulo.
2. Abra `ATIVIDADES.md` e faça o checkpoint do Bloco 1 **no papel**.
3. Só então entre em `TEORIA_PASSO_A_PASSO.md` do primeiro módulo.
4. Implemente TODOs na ordem do mapa da RESOLUCAO; não leia `solutions/` antes.
5. Feche o bloco com o teste e volte ao checkpoint do próximo bloco.

## Comandos de validação

```powershell
python scripts/pedagogy_check_unified.py --day {day.name}
python scripts/run_day_tests.py --day {day.name} --mode solutions
```

## Se travar

Use a seção **Onde colocar** da RESOLUCAO (arquivo + função + substituir). Se a seção não nomear o arquivo, o artefato está incompleto — reporte; não invente outro path.
"""
    path.write_text(body.rstrip() + extra + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    for dname in DAYS:
        day = ROOT / "days" / dname
        if not day.is_dir():
            continue
        deepen_atividades(day)
        deepen_start_here(day)
        for res in day.glob("*/*/RESOLUCAO_GUIADA_PASSO_A_PASSO.md"):
            mod = res.parent
            teoria = mod / "TEORIA_PASSO_A_PASSO.md"
            ex = mod / "EXERCICIOS.md"
            if teoria.exists():
                t = teoria.read_text(encoding="utf-8")
                teoria.write_text(deepen_teoria(mod, t), encoding="utf-8", newline="\n")
            r = res.read_text(encoding="utf-8")
            res.write_text(deepen_resolucao(mod, r), encoding="utf-8", newline="\n")
            if ex.exists():
                e = ex.read_text(encoding="utf-8")
                ex.write_text(deepen_exercicios(e), encoding="utf-8", newline="\n")
        print("deepened", dname)


if __name__ == "__main__":
    main()
