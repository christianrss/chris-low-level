#include "clvm_format.h"

#include <stdio.h>
#include <string.h>

static uint16_t read_u16_le(const uint8_t *bytes) {
    return (uint16_t)bytes[0] | ((uint16_t)bytes[1] << 8U);
}

static uint32_t read_u32_le(const uint8_t *bytes) {
    return (uint32_t)bytes[0] |
           ((uint32_t)bytes[1] << 8U) |
           ((uint32_t)bytes[2] << 16U) |
           ((uint32_t)bytes[3] << 24U);
}

static int fail(char *error, size_t capacity, const char *message) {
    if (error != NULL && capacity > 0U) {
        snprintf(error, capacity, "%s", message);
    }
    return 0;
}

uint32_t clvm_fnv1a32(const uint8_t *data, size_t size) {
    uint32_t hash = 2166136261u;

    for (size_t i = 0; i < size; ++i) {
        hash ^= data[i];
        hash *= 16777619u;
    }

    return hash;
}

int clvm_parse(
    const uint8_t *file,
    size_t file_size,
    clvm_image *out,
    char *error,
    size_t error_capacity) {

    // Never trust lengths from a binary file before checking the real buffer.
    if (file == NULL || out == NULL) {
        return fail(error, error_capacity, "null argument");
    }
    if (file_size < CLVM_HEADER_SIZE) {
        return fail(error, error_capacity, "file too small");
    }
    if (memcmp(file, "CLVM", 4) != 0) {
        return fail(error, error_capacity, "bad magic");
    }

    clvm_image image;
    image.version = file[4];
    image.flags = file[5];
    image.entry = read_u16_le(file + 6);
    image.code_size = read_u32_le(file + 8);
    image.checksum = read_u32_le(file + 12);
    image.code = file + CLVM_HEADER_SIZE;

    if (image.version != CLVM_VERSION) {
        return fail(error, error_capacity, "unsupported version");
    }
    if (image.flags != 0U) {
        return fail(error, error_capacity, "unsupported flags");
    }
    if ((size_t)image.code_size != file_size - CLVM_HEADER_SIZE) {
        return fail(error, error_capacity, "size mismatch");
    }
    if (image.entry >= image.code_size && image.code_size != 0U) {
        return fail(error, error_capacity, "entry outside code");
    }
    if (clvm_fnv1a32(image.code, image.code_size) != image.checksum) {
        return fail(error, error_capacity, "checksum mismatch");
    }

    *out = image;
    return 1;
}
