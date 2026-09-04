# Gabarito - IA

- Forward: `pred=7`, `error=-3`, `loss=9`.
- Gradientes: `dL/dw=-12`, `dL/db=-6`.
- Um passo de SGD com `lr=0.01`: `w=3.12`, `b=1.06`.
- O dataset segue `y=2x+1`.
- `float tensor[32][128]`: 4096 elementos, 16384 bytes, 16 KiB.
- No bug de backward, `d_weight` perdeu o fator `x` e `d_bias` recebeu esse fator indevidamente. Para MSE média, os gradientes do batch também devem ser divididos pelo número de amostras.
