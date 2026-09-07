// REVIEW ONLY: not built/loaded in this environment.
// Compare with userspace hid_kbd.c — real kernel uses hidinput_report_raw and input_report_key.
#include <linux/module.h>
#include <linux/hid.h>
#include <linux/input.h>

static int chris_kbd_probe(struct hid_device* hid, const struct hid_device_id* id) {
    return hid_parse(hid);
}

static int chris_kbd_event(struct hid_device* hid, struct hid_field* field,
                           struct hid_usage* usage, __s32 value) {
    struct input_dev* input = hid->input;
    if (!input) {
        return 0;
    }
    input_report_key(input, usage->code, value);
    input_sync(input);
    return 0;
}

static const struct hid_device_id chris_kbd_ids[] = {
    { HID_USB_DEVICE(0x046d, 0xc31c) },
    { }
};
MODULE_DEVICE_TABLE(hid, chris_kbd_ids);

static struct hid_driver chris_kbd_driver = {
    .name = "chris_hid_kbd",
    .id_table = chris_kbd_ids,
    .probe = chris_kbd_probe,
    .event = chris_kbd_event,
};

static int __init chris_kbd_init(void) {
    return hid_register_driver(&chris_kbd_driver);
}

static void __exit chris_kbd_exit(void) {
    hid_unregister_driver(&chris_kbd_driver);
}

module_init(chris_kbd_init);
module_exit(chris_kbd_exit);
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Chris Lab");
