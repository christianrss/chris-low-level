// PEDAGOGY-SOLUTION: KMOD-MODEL-OPEN-01
// PEDAGOGY-SOLUTION: KMOD-MODEL-IO-02
// PEDAGOGY-SOLUTION: KMOD-SOURCE-REVIEW-03
#include "device_model.h"
#include <stdio.h>
#include <string.h>

static int lifecycle_trace_enabled = 0;

void device_set_trace(int enabled) {
    lifecycle_trace_enabled = enabled;
}

void device_trace(const char* event, Device* dev) {
    if (!lifecycle_trace_enabled) {
        return;
    }
    fprintf(
        stderr,
        "[kmod-trace] %s open=%d len=%zu\n",
        event,
        dev->is_open,
        dev->length);
}

int device_open(Device* dev) {
    if (dev->is_open) {
        return -1;
    }
    dev->is_open = 1;
    device_trace("open", dev);
    return 0;
}

void device_release(Device* dev) {
    device_trace("release", dev);
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
    device_trace("write", dev);
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
    device_trace("read", dev);
    return (int)count;
}
