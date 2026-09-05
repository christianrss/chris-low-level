// TODO [KMOD-MODEL-OPEN-01] [KMOD-MODEL-IO-02]
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
    // TODO [KMOD-MODEL-OPEN-01]
    device_trace("open", dev);
    return -1;
}

void device_release(Device* dev) {
    device_trace("release", dev);
    dev->is_open = 0;
}

int device_write(Device* dev, const void* src, size_t count) {
    // TODO [KMOD-MODEL-IO-02]
    device_trace("write", dev);
    return -1;
}

int device_read(Device* dev, void* dst, size_t count) {
    // TODO [KMOD-MODEL-IO-02]
    device_trace("read", dev);
    return -1;
}
