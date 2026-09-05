#include "device_model.h"
#include <string.h>
int device_open(Device*d){/* TODO [KMOD-MODEL-OPEN-01] */ return 0;}
int device_release(Device*d){d->is_open=0; return 0;}
int device_write(Device*d,const unsigned char*s,size_t n){/* TODO [KMOD-MODEL-IO-02] */ return -1;}
int device_read(Device*d,unsigned char*out,size_t n){/* TODO [KMOD-MODEL-IO-02] */ return -1;}
