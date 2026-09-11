#pragma once
enum ShaderStage { ST_EDIT = 0, ST_COMPILE = 1, ST_LINK = 2, ST_READY = 3 };
int shader_can(int from, int to);
int shader_apply(int *stage, int to);
int shader_illegal(int from, int to);
