#include <stdint.h>
#include <stdio.h>
#include <string.h>

/*
 * Benign reversing target.
 *
 * The verification routine intentionally performs a small byte transform so
 * the student can recover it from assembly. It has no security purpose.
 */
static int verify_code(const char *input) {
    static const uint8_t expected[] = {
        0x5D, 0x4A, 0x5B, 0x5A, 0x47, 0x12, 0x1B, 0x1C,
    };

    const size_t expected_length = sizeof(expected) / sizeof(expected[0]);
    if (strlen(input) != expected_length) {
        return 0;
    }

    for (size_t i = 0; i < expected_length; ++i) {
        const uint8_t transformed =
            (uint8_t)(((uint8_t)input[i] ^ 0x2AU) + (uint8_t)i);

        if (transformed != expected[i]) {
            return 0;
        }
    }

    return 1;
}

int main(int argc, char **argv) {
    puts("LOWLEVEL-REVERSING-LAB-V1");

    if (argc != 2) {
        fprintf(stderr, "usage: lab_target <code>\n");
        return 2;
    }

    if (verify_code(argv[1])) {
        puts("accepted");
        return 0;
    }

    puts("rejected");
    return 1;
}
