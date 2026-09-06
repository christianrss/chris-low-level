#ifndef CLVM_FORMAT_H
#define CLVM_FORMAT_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Fixed-size disk header for CLVM v1. Multi-byte fields are little-endian. */
#define CLVM_HEADER_SIZE 16u
#define CLVM_VERSION 1u

/* Parsed view: code points into the caller-owned input buffer. */
typedef struct {
    uint8_t version;
    uint8_t flags;
    uint16_t entry;
    uint32_t code_size;
    uint32_t checksum;
    const uint8_t *code;
} clvm_image;

/* FNV-1a is used only as an integrity checksum, not as cryptography. */
uint32_t clvm_fnv1a32(const uint8_t *data, size_t size);

/* Validate the file before exposing a code pointer to the VM. */
int clvm_parse(
    const uint8_t *file,
    size_t file_size,
    clvm_image *out,
    char *err,
    size_t err_cap);

#ifdef __cplusplus
}
#endif

#endif
