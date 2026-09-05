# Teoria passo a passo

## 1. Streams em Node
Streams permitem processar dados incrementalmente. `Transform` recebe chunks, produz outros chunks e mantém estado entre chamadas. Nosso `LineTransform` precisa lidar com linhas que atravessam fronteiras de chunk.

## 2. UTF-8 e chunk boundaries
Um caractere multibyte como `€` pode chegar dividido. `StringDecoder` guarda bytes incompletos e só devolve texto válido quando há bytes suficientes. Concatenar `chunk.toString()` ingenuamente pode corromper caracteres.

## 3. Buffer lógico de linha
`this.pending` guarda o fragmento que ainda não terminou em `\n`. A cada `_transform`, combine pending + texto decodificado, separe linhas completas e retenha a cauda. `_flush` entrega o restante no fim do stream.

## 4. Backpressure
Em Writable, `write()` retornar `false` significa que o buffer interno passou do limite de pressão. O produtor deve parar e aguardar `drain`. Ignorar isso pode aumentar memória e latência. O arquivo `backpressure_demo.js` existe de verdade no starter/solution para observar esse mecanismo.

## 5. Relação com libuv
O stream é uma abstração JS construída sobre event loop e I/O assíncrono. A trilha futura desce para libuv, handles, requests e filas do event loop.