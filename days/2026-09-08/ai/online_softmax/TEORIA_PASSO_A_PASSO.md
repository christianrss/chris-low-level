# Teoria passo a passo — Online softmax

Softmax ingênuo calcula `exp(x_i)` diretamente e pode overflow. A forma estável subtrai o máximo:
`softmax_i = exp(x_i-m)/sum_j exp(x_j-m)`. Online softmax mantém máximo e denominador em uma única passagem.

Ao processar novo x:
```text
m_new = max(m, x)
d_new = d * exp(m - m_new) + exp(x - m_new)
```
O fator `exp(m-m_new)` reescala a soma antiga para a nova referência. Depois uma segunda passagem produz as
probabilidades com `exp(x_i-m)/d`.

Isso é útil para entender kernels de attention: FlashAttention explora ideias relacionadas de estatísticas online
por blocos, embora este laboratório seja apenas vetor 1D em CPU.

Invariantes: `d > 0` depois do primeiro elemento, `m` é máximo visto, e a soma final das probabilidades deve ser
aproximadamente 1. Vetor vazio é erro explícito.
