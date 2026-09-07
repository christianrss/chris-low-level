# Pesquisa guiada — explicit GPU synchronization

## Fontes primárias / técnicas
- Vulkan Synchronization chapter
- Microsoft D3D12 resource barriers docs

## Perguntas antes de implementar
1. O que state tracker sabe e o driver não adivinha?
2. Por que barrier redundante custa?
3. Layout Vulkan e state D3D12 são idênticos?

## Depois
Explique quais simplificações o laboratório faz, qual invariante protege correção e qual métrica você mediria antes de otimizar.
