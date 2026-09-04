# Teoria passo a passo - Assembly x86-64 e ABI

## 1. O que e ABI
A ISA define instrucoes; a ABI define como programas combinam essas instrucoes para chamar funcoes, passar argumentos, retornar valores e preservar registradores. No System V AMD64, os primeiros argumentos inteiros/ponteiros chegam em RDI, RSI, RDX, RCX, R8 e R9; o retorno inteiro usa RAX.

## 2. O exercicio
A funcao recebe `(ponteiro, quantidade)`. O ponteiro aponta para `uint64_t`, portanto avancar para o proximo item significa somar 8 ao endereco. A soma usa overflow modular de 64 bits, exatamente como `uint64_t` em C.

## 3. Registradores
RDI: endereco atual. RSI: itens restantes. RAX: acumulador/retorno. Como todos sao caller-saved nesta ABI, nao precisamos salvar registradores callee-saved.

## 4. Testes
Teste lista normal, quantidade zero e overflow modular. Depois compare a funcao Assembly com uma referencia C sobre entradas aleatorias.
