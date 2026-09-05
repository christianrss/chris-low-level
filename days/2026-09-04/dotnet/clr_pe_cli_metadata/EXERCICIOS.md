# Exercícios — PE/CLI metadata (BSJB)

## Fácil

- Desenhe o mapa MZ → PE → DataDirectory[14] → CLI Header → Metadata BSJB para a fixture de teste (RVAs 0x2100 e 0x2200).
- Abra `CliPeInspector.cs` e explique o que `RequireRange` impede.

## Médio

- **D2-CLR-CLI-RVA:** converta `cliRva` para file offset usando `RvaToOffset` já fornecido.
- Calcule manualmente: VA=0x2000, Raw=0x200, RVA=0x2100 → offset esperado.

## Difícil

- **D2-CLR-METADATA-RVA:** converta `metadataRva` e valide assinatura `BSJB` no offset resultante.
- Documente o que acontece se você usar RVA como file offset direto (bug clássico).

## Desafio

- Gere PE sintético com 3 sections e meça tempo de `Inspect()` — compare hipótese linear vs. número de sections.
- Pesquise ECMA-335: o que vem imediatamente após a assinatura BSJB no metadata root?
