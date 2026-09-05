/* TESTS [KMOD-MODEL-OPEN-01] [KMOD-MODEL-IO-02] */
#include "device_model.h"
#include <assert.h>
#include <string.h>
#include <stdio.h>
int main(){Device d={0}; assert(device_open(&d)==0); assert(device_open(&d)==-1); unsigned char s[]="abc",o[8]={0}; assert(device_write(&d,s,3)==3); assert(device_read(&d,o,8)==3); assert(memcmp(o,"abc",3)==0); assert(device_release(&d)==0); assert(device_read(&d,o,1)==-1); puts("OK device model");}
