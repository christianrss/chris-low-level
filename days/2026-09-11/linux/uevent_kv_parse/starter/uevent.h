#ifndef UEVENT_H
#define UEVENT_H
#include <stddef.h>
#define UEVENT_MAX 16
#define UEVENT_KEY 32
#define UEVENT_VAL 64
typedef struct { char key[UEVENT_KEY]; char val[UEVENT_VAL]; } UeventKV;
int uevent_parse_line(const char *line, UeventKV *out);
int uevent_parse_block(const char *block, UeventKV *table, int cap, int *out_n);
const char *uevent_get(const UeventKV *table, int n, const char *key);
#endif
