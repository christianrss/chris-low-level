// SOLVES [KMOD-MODEL-OPEN-01]
// SOLVES [KMOD-MODEL-IO-02]
// SOLVES [KMOD-SOURCE-REVIEW-03]
#include "device_model.h"
#include <string.h>

int device_open(Device* dev) {
    if (dev->is_open) {
        return -1;
    }
    dev->is_open = 1;
    return 0;
}

void device_release(Device* dev) {
    dev->is_open = 0;
}

int device_write(Device* dev, const void* src, size_t count) {
    if (!dev->is_open) {
        return -1;
    }
    if (count > sizeof dev->buffer) {
        count = sizeof dev->buffer;
    }
    memcpy(dev->buffer, src, count);
    dev->length = count;
    return (int)count;
}

int device_read(Device* dev, void* dst, size_t count) {
    if (!dev->is_open) {
        return -1;
    }
    if (count > dev->length) {
        count = dev->length;
    }
    memcpy(dst, dev->buffer, count);
    return (int)count;
}
