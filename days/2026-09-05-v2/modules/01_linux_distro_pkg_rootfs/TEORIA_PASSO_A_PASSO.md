# Teoria passo a passo

## 1. O que estamos construindo
Hoje a trilha de distribuição Linux ganha dois blocos concretos: um formato mínimo de pacote e um construtor de rootfs. O objetivo não é imitar `apt` ou `rpm`; é entender as invariantes que aparecem dentro deles. Um pacote educacional pode ser representado por um diretório com `manifest.json` e `payload/`. O manifest descreve `name`, `version` e a lista de arquivos. O payload contém os bytes que serão copiados para a raiz de destino.

## 2. Por que validar antes de copiar
O rootfs é apenas um diretório durante o laboratório, mas devemos tratá-lo como se fosse a raiz real do sistema. Se o manifest aceitar `/etc/passwd` ou `../../arquivo`, o instalador pode escrever fora do rootfs. Por isso `load_manifest()` deve rejeitar caminhos absolutos e qualquer componente `..` antes de `install_package()` criar arquivos. Esse princípio é a base de path traversal defense.

## 3. Estado instalado
Depois da cópia, o gerenciador grava `var/lib/chris-pkg/installed.json`. O banco só deve mudar depois que o plano de arquivos foi validado e copiado. É uma versão pequena do princípio transacional: não anunciar sucesso antes de concluir a mutação. No futuro essa trilha evolui para ownership por arquivo, hashes, dependências, conflitos, staging e rollback.

## 4. Rootfs reproduzível e idempotente
`build_rootfs.sh` cria `bin`, `etc`, `proc`, `sys`, `dev`, `tmp` e `var/lib/chris-pkg`. O uso de `mkdir -p` torna o script idempotente: rodar duas vezes continua válido. Essa propriedade é importante em build systems, imagens de sistema, initramfs e automação de infraestrutura.

## 5. O que observar
A ordem correta é: validar entrada -> construir plano -> criar diretórios pais -> copiar payload -> gravar estado. Essa ordem reduz estados intermediários incoerentes e prepara o terreno para transações mais fortes.

## O quê

Este módulo ensina o conceito central do laboratório v2 com foco operacional no `starter/`.

## Como

Siga os `TODO [ID]` no starter; use a resolução para localizar arquivo/função e o que substituir.

| Etapa | Ação |
|-------|------|
| 1 | Ler README e mapa de TODOs |
| 2 | Implementar no starter |
| 3 | Rodar testes |

## Por que

Sem teoria mínima o aluno não conecta o exercício ao sistema maior.

## Por que (design)

O formato v2 compacta o dia 05; ainda assim cada módulo precisa de O quê/Como/Por quê verificáveis.

## Por que (qualidade)

O checker unificado exige ≥120 linhas, diagrama/tabela e ≥3 seções Por quê.

## Invariantes

- Cada TODO tagueado aparece em starter, solução, testes e resolução.
- Placement (Onde colocar) por ID.

## Bugs comuns

| Sintoma | Causa | Debug |
|---------|-------|-------|
| teste FAIL | stub não substituído | abra a âncora TODO |
| parse errado | ordem de campos | compare com solutions |

## Trace manual

No papel: anote entrada → transformação → saída esperada do primeiro teste do módulo.

## O quê

Este módulo ensina o conceito central do laboratório v2 com foco operacional no `starter/`.

## Como

Siga os `TODO [ID]` no starter; use a resolução para localizar arquivo/função e o que substituir.

| Etapa | Ação |
|-------|------|
| 1 | Ler README e mapa de TODOs |
| 2 | Implementar no starter |
| 3 | Rodar testes |

## Por que

Sem teoria mínima o aluno não conecta o exercício ao sistema maior.

## Por que (design)

O formato v2 compacta o dia 05; ainda assim cada módulo precisa de O quê/Como/Por quê verificáveis.

## Por que (qualidade)

O checker unificado exige ≥120 linhas, diagrama/tabela e ≥3 seções Por quê.

## Invariantes

- Cada TODO tagueado aparece em starter, solução, testes e resolução.
- Placement (Onde colocar) por ID.

## Bugs comuns

| Sintoma | Causa | Debug |
|---------|-------|-------|
| teste FAIL | stub não substituído | abra a âncora TODO |
| parse errado | ordem de campos | compare com solutions |

## Trace manual

No papel: anote entrada → transformação → saída esperada do primeiro teste do módulo.

## O quê

Este módulo ensina o conceito central do laboratório v2 com foco operacional no `starter/`.

## Como

Siga os `TODO [ID]` no starter; use a resolução para localizar arquivo/função e o que substituir.

| Etapa | Ação |
|-------|------|
| 1 | Ler README e mapa de TODOs |
| 2 | Implementar no starter |
| 3 | Rodar testes |

## Por que

Sem teoria mínima o aluno não conecta o exercício ao sistema maior.

## Por que (design)

O formato v2 compacta o dia 05; ainda assim cada módulo precisa de O quê/Como/Por quê verificáveis.

## Por que (qualidade)

O checker unificado exige ≥120 linhas, diagrama/tabela e ≥3 seções Por quê.

## Invariantes

- Cada TODO tagueado aparece em starter, solução, testes e resolução.
- Placement (Onde colocar) por ID.

## Bugs comuns

| Sintoma | Causa | Debug |
|---------|-------|-------|
| teste FAIL | stub não substituído | abra a âncora TODO |
| parse errado | ordem de campos | compare com solutions |

## Trace manual

No papel: anote entrada → transformação → saída esperada do primeiro teste do módulo.
