#pragma once
#include <stddef.h>
typedef struct { int is_open; size_t length; unsigned char buffer[64]; } Device;
int device_open(Device*); void device_release(Device*); int device_write(Device*,const void*,size_t); int device_read(Device*,void*,size_t);
