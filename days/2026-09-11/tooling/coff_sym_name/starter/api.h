#ifndef COFF_API_H
#define COFF_API_H
#ifdef __cplusplus
extern "C" {
#endif
/* RCX = pointer to 8-byte COFF name field (Windows x64) */
int coff_name_is_short(const unsigned char *field);
int coff_short_name_len(const unsigned char *field);
/* returns 1 if first 4 bytes zero (long name via string table offset) */
int coff_name_is_long(const unsigned char *field);
#ifdef __cplusplus
}
#endif
#endif
