#include "shader_fsm.hpp"
int shader_can(int from, int to) {
    // PEDAGOGY-SOLUTION: GFX-SHADER-FSM-01
    if (from == ST_EDIT && to == ST_COMPILE) return 1;
    if (from == ST_COMPILE && (to == ST_LINK || to == ST_EDIT)) return 1;
    if (from == ST_LINK && to == ST_READY) return 1;
    if (from == ST_READY && to == ST_EDIT) return 1;
    return 0;
}
int shader_apply(int *stage, int to) {
    // PEDAGOGY-SOLUTION: GFX-SHADER-FSM-02
    if (!stage || !shader_can(*stage, to)) return -1;
    *stage = to;
    return 0;
}
int shader_illegal(int from, int to) {
    // PEDAGOGY-SOLUTION: GFX-SHADER-FSM-03
    return shader_can(from, to) ? 0 : 1;
}
