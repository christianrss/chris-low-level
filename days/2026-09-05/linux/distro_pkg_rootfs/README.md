# Linux distro: pacote próprio + rootfs reproduzível

**Objetivo:** Criar o primeiro formato de pacote da `chris-linux-distro`, instalar o payload em um rootfs de staging e gerar esse rootfs por script idempotente.

## Ordem recomendada
1. `TEORIA_PASSO_A_PASSO.md`
2. `PESQUISA_GUIADA.md`
3. starter
4. `RESOLUCAO_GUIADA_PASSO_A_PASSO.md`
5. `TESTES_GUIADOS.md`
6. `solutions/` somente como gabarito final

## TODOs auditáveis
- `LINUX-PKG-PARSE-01`
- `LINUX-PKG-INSTALL-02`
- `LINUX-ROOTFS-BUILD-03`

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-linux-pkg/day03` |
| O que levar | pkg parser + rootfs builder |
| Testes a replicar | test_pkg.py + test_rootfs.sh |
| Milestone | linux pkg milestone |
| Commit sugerido | `feat(linux): port pkg/rootfs from day05 lab` |

Após portar, marque no **Relatório de resolução**: *Portei para projects/? Sim/Não — evidência: comando de teste que passou*.
