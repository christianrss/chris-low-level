#include "shader_fsm.hpp"
#include <assert.h>
#include <stdio.h>
// PEDAGOGY-TEST: GFX-SHADER-FSM-01
// PEDAGOGY-TEST: GFX-SHADER-FSM-02
// PEDAGOGY-TEST: GFX-SHADER-FSM-03
int main() {
    int s = ST_EDIT;
    assert(shader_can(ST_EDIT, ST_COMPILE) == 1);
    assert(shader_can(ST_EDIT, ST_READY) == 0);
    assert(shader_apply(&s, ST_COMPILE) == 0 && s == ST_COMPILE);
    assert(shader_apply(&s, ST_READY) == -1 && s == ST_COMPILE);
    assert(shader_illegal(ST_EDIT, ST_READY) == 1);
    printf("OK shader fsm\n");
    return 0;
}
