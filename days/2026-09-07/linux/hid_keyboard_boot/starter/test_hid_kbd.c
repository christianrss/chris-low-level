// PEDAGOGY-TEST: HID-KBD-DECODE-01
// PEDAGOGY-TEST: HID-KBD-MAP-02
// PEDAGOGY-TEST: HID-KBD-RING-03
// PEDAGOGY-TEST: HID-KBD-READ-04
// PEDAGOGY-TEST: HID-KBD-DECODE-01: parse 8-byte boot report into HidBootReport
// PEDAGOGY-TEST: HID-KBD-MAP-02: press/release KEY_A from report transitions
// PEDAGOGY-TEST: HID-KBD-RING-03: push events into fixed-capacity ring
// PEDAGOGY-TEST: HID-KBD-READ-04: read() drains InputEvent records FIFO
// Test cases (TESTES_GUIADOS.md):
// Caso 1: Compile e execute hid_kbd_test em starter/ (falha até implementar TODOs).
// Caso 2: Carregue fixture report_a_press.raw e valide decode de usage 0x04.
// Caso 3: Transição press→release gera EV_KEY KEY_A value 1 depois 0.
// Caso 4: Ring cheio retorna -1 em push; read esvazia em ordem.
// Caso 5: sizeof(InputEvent)==24 (layout evdev simplificado).
// Caso 6: Valide solutions/ com os mesmos asserts.
#include "hid_kbd.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>

#ifndef FIXTURES_DIR
#define FIXTURES_DIR "fixtures"
#endif

static int load_fixture(const char* name, uint8_t* buf, size_t len) {
    char path[512];
    snprintf(path, sizeof path, "%s/%s", FIXTURES_DIR, name);
    FILE* f = fopen(path, "rb");
    if (!f) {
        return -1;
    }
    size_t n = fread(buf, 1, len, f);
    fclose(f);
    return (n == len) ? 0 : -1;
}

static void push_mapped(HidKbdRing* ring, const HidBootReport* cur, const HidBootReport* prev) {
    InputEvent batch[16];
    ssize_t n = hid_kbd_map_events(cur, prev, batch, 16);
    assert(n >= 0);
    for (ssize_t i = 0; i < n; ++i) {
        assert(hid_kbd_ring_push(ring, &batch[i]) == 0);
    }
}

int main(void) {
    assert(sizeof(InputEvent) == 24);

    uint8_t press_raw[8] = {0};
    uint8_t empty_raw[8] = {0};
    assert(load_fixture("report_a_press.raw", press_raw, 8) == 0);
    assert(load_fixture("report_empty.raw", empty_raw, 8) == 0);

    HidBootReport empty = {0};
    HidBootReport press = {0};
    hid_kbd_set_time(1000);
    hid_boot_parse_report(press_raw, &press);
    assert(press.keys[0] == 0x04);

    InputEvent ev[4] = {0};
    ssize_t mapped = hid_kbd_map_events(&press, &empty, ev, 4);
    assert(mapped == 1);
    assert(ev[0].type == EV_KEY);
    assert(ev[0].code == KEY_A);
    assert(ev[0].value == 1);

    HidBootReport release = {0};
    hid_boot_parse_report(empty_raw, &release);
    mapped = hid_kbd_map_events(&release, &press, ev, 4);
    assert(mapped == 1);
    assert(ev[0].type == EV_KEY);
    assert(ev[0].code == KEY_A);
    assert(ev[0].value == 0);

    HidKbdRing ring = {0};
    push_mapped(&ring, &press, &empty);
    push_mapped(&ring, &release, &press);

    InputEvent out[4] = {0};
    ssize_t rd = hid_kbd_ring_read(&ring, out, 4);
    assert(rd == 2);
    assert(out[0].value == 1);
    assert(out[1].value == 0);

    InputEvent dummy = {0};
    for (int i = 0; i < HID_KBD_RING_CAP; ++i) {
        dummy.value = (int32_t)i;
        assert(hid_kbd_ring_push(&ring, &dummy) == 0);
    }
    assert(hid_kbd_ring_push(&ring, &dummy) == -1);

    puts("OK hid keyboard boot");
    return 0;
}
