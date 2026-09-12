# Proposal: dias futuros orientados a profundidade

## Problema

O contrato tier-A atual exige pelo menos 13 módulos e até 12 trilhas no
mesmo dia. Na prática, os dias recentes chegaram a 23–24 módulos e
46–69 horas, enquanto vários exercícios se reduziram a três stubs e
documentação preenchida até um limite de linhas.

Isso contradiz a regra de ouro do repositório: menos experiências,
ensinadas com profundidade e executáveis sem assistência externa.

## Solução

Introduzir o perfil `depth_first` para dias posteriores a 2026-09-11:

- exatamente um projeto principal por dia;
- carga planejada de 6–8 horas;
- starter quase vazio, com infraestrutura e contratos, mas sem o núcleo;
- 6–10 marcos de construção end-to-end;
- no mínimo 250 linhas substantivas de trabalho esperado do aluno;
- cobertura curricular por ciclo de 7–10 dias, não por matriz diária;
- avaliação baseada em comportamento, falhas, integração e benchmark.

Os dias 2026-09-03 a 2026-09-11 permanecem como acervo legado e não
serão reescritos por esta mudança.

## Compatibilidade

O perfil tier-A e suas regras por data continuam válidos para os dias
legados. Validadores novos selecionam `depth_first` somente por contrato
explícito ou para datas a partir de `2026-09-12`.

## Critérios de sucesso

1. Um fixture `depth_first` válido passa contrato, pedagogia e ciclo.
2. Fixtures com dois projetos, starter pré-resolvido, padding, poucos
   testes, skip indevido ou falhas inesperadas são rejeitados.
3. Resultados dos gates legados são comparados antes/depois sem editar
   o conteúdo dos dias antigos.
4. CI descobre automaticamente novos dias `depth_first`.
5. Nenhum scaffold gera teoria, resolução ou exercícios preenchidos.

## Fora de escopo

- reescrever os dias existentes;
- escolher o tema do primeiro novo dia;
- bloquear tecnicamente o acesso local a `solutions/`;
- exigir DOCX como fonte pedagógica.
