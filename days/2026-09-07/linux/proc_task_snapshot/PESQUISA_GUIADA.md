# Pesquisa guiada — /proc process accounting

## Fontes primárias / técnicas
- man proc_pid_stat(5)
- man proc(5)

## Perguntas antes de implementar
1. Por que split simples quebra comm?
2. O que é PID reuse?
3. Por que snapshot precisa ser tolerante a ENOENT?

## Depois
Explique quais simplificações o laboratório faz, qual invariante protege correção e qual métrica você mediria antes de otimizar.
