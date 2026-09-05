// PEDAGOGY-TEST: OBJDUMP-U16-01
// PEDAGOGY-TEST: OBJDUMP-U32-01
// PEDAGOGY-TEST: OBJDUMP-PARSE-01
#include <stdio.h>

static int add_then_double(int a, int b) {
    const int sum = a + b;
    return sum * 2;
}

int main(void) {
    const int value = add_then_double(7, 12);
    printf("value=%d\n", value);
    return value == 38 ? 0 : 1;
}
