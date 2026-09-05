# Rubrica de review — KMOD-SOURCE-REVIEW-03

Use esta rubrica ao revisar `starter/chris_char.c` e `solutions/chris_char.c`.

| Critério | 0 — Ausente | 1 — Parcial | 2 — Completo |
|----------|-------------|-------------|--------------|
| `module_init` / `module_exit` | Não existem | Existem mas sem cleanup | Registram e liberam chrdev |
| `file_operations` | Não conectadas | Só open/release | open, release, read, write |
| Tratamento de erro | Ignora retornos | Alguns checks | Todos os erros propagados |
| `copy_to_user` / `copy_from_user` | Não usa | Uso incorreto | Uso correto com validação |
| Licença / metadados | Ausente | GPL sem autor | MODULE_LICENSE + AUTHOR |

## Perguntas de review

1. O major/minor é liberado em `module_exit`?
2. O buffer do device é protegido contra overflow?
3. Há race entre open concorrentes?
4. O código compila contra headers do kernel alvo?

## Evidência esperada

- Trace de lifecycle em userspace (`device_set_trace(1)`) correlacionado com o fluxo do módulo.
- Checklist preenchido no Relatório de resolução.
