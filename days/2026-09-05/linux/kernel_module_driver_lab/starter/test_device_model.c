// PEDAGOGY-TEST: KMOD-MODEL-OPEN-01: double-open retorna -1
// PEDAGOGY-TEST: KMOD-MODEL-IO-02: read/write só com device aberto
// PEDAGOGY-TEST: KMOD-MODEL-OPEN-01: open exclusivo e rejeição de double-open
// PEDAGOGY-TEST: KMOD-MODEL-IO-02: read/write com dispositivo fechado retorna -1
// Test cases (TESTES_GUIADOS.md):
// Caso 1: Compile e execute `test_device_model` em starter/ (falha até implementar TODOs).
// Caso 2: Ative trace: `device_set_trace(1)` imprime `[kmod-trace]` no stderr.
// Caso 3: **Double-open:** segundo `device_open` retorna -1.
// Caso 4: **I/O fechado:** `device_read` após `device_release` retorna -1.
// Caso 5: Revise `chris_char.c` com `REVIEW_RUBRIC.md` (KMOD-SOURCE-REVIEW-03).
// Caso 6: Valide solutions/ com os mesmos asserts.
#include "device_model.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    Device dev = {0};
    char out[8] = {0};

    device_set_trace(1);

    assert(device_open(&dev) == 0);
    assert(device_open(&dev) == -1);
    assert(device_write(&dev, "abc", 3) == 3);
    assert(device_read(&dev, out, 3) == 3);
    assert(memcmp(out, "abc", 3) == 0);

    device_release(&dev);
    assert(device_read(&dev, out, 1) == -1);

    puts("OK kmod model");
    return 0;
}