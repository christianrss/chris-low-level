#pragma once
#include <stddef.h>

typedef struct {
    int is_open;
    size_t length;
    unsigned char buffer[64];
} Device;

void device_set_trace(int enabled);
void device_trace(const char* event, Device* dev);
int device_open(Device* dev);
void device_release(Device* dev);
int device_write(Device* dev, const void* src, size_t count);
int device_read(Device* dev, void* dst, size_t count);
