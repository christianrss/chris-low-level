// PEDAGOGY-TEST [KMOD-MODEL-OPEN-01]: double-open retorna -1
// PEDAGOGY-TEST [KMOD-MODEL-IO-02]: read/write só com device aberto
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
