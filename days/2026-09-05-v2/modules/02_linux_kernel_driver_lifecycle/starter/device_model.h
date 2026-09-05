#pragma once
#include <stddef.h>
typedef struct { int is_open; unsigned char buffer[64]; size_t length; } Device;
int device_open(Device*); int device_release(Device*); int device_write(Device*,const unsigned char*,size_t); int device_read(Device*,unsigned char*,size_t);
