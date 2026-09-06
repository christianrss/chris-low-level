#include "clvm_format.h"
#include <stdio.h>
#include <string.h>

static uint16_t read_u16_le(const uint8_t *p) { return (uint16_t)p[0] | ((uint16_t)p[1] << 8); }
static uint32_t read_u32_le(const uint8_t *p) { return (uint32_t)p[0] | ((uint32_t)p[1]<<8) | ((uint32_t)p[2]<<16) | ((uint32_t)p[3]<<24); }
static int fail(char *err,size_t cap,const char *msg){ if(err&&cap) snprintf(err,cap,"%s",msg); return 0; }

uint32_t clvm_fnv1a32(const uint8_t *data, size_t size) {
    /* TODO [CLVM-C-FNV-01]: implement the same FNV-1a used by tools/assemble.py. */
    uint32_t hash = 2166136261u;

    for (size_t i = 0; i < size; ++i) {
        hash ^= data[i];
        hash *= 16777619u;
    }

    return hash;
}

int clvm_parse(const uint8_t *file,size_t file_size,clvm_image *out,char *err,size_t err_cap){
    if(!file||!out) return fail(err,err_cap,"null argument");
    if(file_size<CLVM_HEADER_SIZE) return fail(err,err_cap,"file too small");
    if(memcmp(file,"CLVM",4)!=0) return fail(err,err_cap,"bad magic");
    clvm_image img={0};
    img.version=file[4]; img.flags=file[5]; img.entry=read_u16_le(file+6);
    img.code_size=read_u32_le(file+8); img.checksum=read_u32_le(file+12); img.code=file+16;
    if(img.version!=CLVM_VERSION) return fail(err,err_cap,"unsupported version");
    if((size_t)img.code_size!=file_size-16) return fail(err,err_cap,"size mismatch");
    /* TODO [CLVM-C-HEADER-01]: reject flags != 0, invalid entry, and checksum mismatch. */
    *out=img; return 1;
}
