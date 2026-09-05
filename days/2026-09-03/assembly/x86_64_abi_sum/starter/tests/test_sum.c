// PEDAGOGY-TEST: ASM-SUM-01
// Test cases (TESTES_GUIADOS.md):
// Caso 1: Escreva um teste do comportamento mais simples antes de adicionar a feature.
// Caso 2: Rode e observe a falha.
// Caso 3: Implemente apenas o necessario para esse teste.
// Caso 4: Adicione edge case/erro relevante.
// Caso 5: Quando encontrar um bug durante o exercicio, transforme-o em regression test ant
#include <assert.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

uint64_t asm_sum_u64(const uint64_t* values, size_t count);

int main(void) {
    const uint64_t values[] = {1, 2, 3, 5, 8, 13};
    assert(asm_sum_u64(values, 6) == 32);
    assert(asm_sum_u64(values, 0) == 0);
    const uint64_t max_pair[] = {UINT64_MAX, 1};
    assert(asm_sum_u64(max_pair, 2) == 0); /* intentional modulo-2^64 overflow */
    puts("assembly ABI tests passed");
    return 0;
}