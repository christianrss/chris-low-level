#include "device_model.h"
#include <string.h>

int device_open(Device* dev) {
    // TODO [KMOD-MODEL-OPEN-01]
    (void)dev;
    return -1;
}

void device_release(Device* dev) {
    dev->is_open = 0;
}

int device_write(Device* dev, const void* src, size_t count) {
    // TODO [KMOD-MODEL-IO-02]
    (void)dev;
    (void)src;
    (void)count;
    return -1;
}

int device_read(Device* dev, void* dst, size_t count) {
    // TODO [KMOD-MODEL-IO-02]
    (void)dev;
    (void)dst;
    (void)count;
    return -1;
}
