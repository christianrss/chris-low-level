# Teoria passo a passo — Chris Debugger Protocol v1

## 1. Separação de responsabilidades
Um debugger de kernel não é apenas uma UI. Precisamos de stub no kernel, transporte, protocolo, cliente host, símbolos, unwinder e crash dump analyzer.

## 2. Framing
Um pacote precisa ser delimitado e validável: magic, versão, command, request id, payload length, checksum e payload.

## 3. Endianness
A versão de hoje serializa inteiros em little-endian explicitamente. Isso evita depender do layout de uma `struct` C++ ou padding do compilador.

## 4. Corrupção
O checksum FNV-1a não é segurança criptográfica; aqui ele serve apenas para detectar corrupção acidental no laboratório.

## 5. Exercícios
**Fácil:** decodifique manualmente um u32 little-endian.  
**Médio:** implemente encoder.  
**Difícil:** implemente decoder com length/checksum validation.  
**Desafio:** projete uma resposta `ReadMemory` com status codes sem quebrar versionamento.
