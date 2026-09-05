/* SOLVES [KMOD-MODEL-OPEN-01] [KMOD-MODEL-IO-02] */
#include "device_model.h"
#include <string.h>
int device_open(Device*d){if(d->is_open)return -1; d->is_open=1; return 0;}
int device_release(Device*d){d->is_open=0; return 0;}
int device_write(Device*d,const unsigned char*s,size_t n){if(!d->is_open)return -1; if(n>sizeof d->buffer)n=sizeof d->buffer; memcpy(d->buffer,s,n); d->length=n; return (int)n;}
int device_read(Device*d,unsigned char*out,size_t n){if(!d->is_open)return -1; if(n>d->length)n=d->length; memcpy(out,d->buffer,n); return (int)n;}
