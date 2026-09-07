// REVIEW ONLY: not built/loaded in this environment.
// Real PS/2 path: serio interrupt → psmouse_packet() → input_report_rel/input_report_key.
#include <linux/module.h>
#include <linux/input.h>
#include <linux/serio.h>

struct chris_ps2_mouse {
    struct input_dev* dev;
    unsigned char packet[3];
    unsigned char count;
};

static irqreturn_t chris_ps2_interrupt(struct serio* serio, unsigned char data, unsigned int flags) {
    struct chris_ps2_mouse* mouse = serio_get_drvdata(serio);
    mouse->packet[mouse->count++] = data;
    if (mouse->count < 3) {
        return IRQ_HANDLED;
    }
    mouse->count = 0;
    input_report_rel(mouse->dev, REL_X, (signed char)mouse->packet[1]);
    input_report_rel(mouse->dev, REL_Y, (signed char)mouse->packet[2]);
    input_sync(mouse->dev);
    return IRQ_HANDLED;
}

static int chris_ps2_connect(struct serio* serio, struct serio_driver* drv) {
    struct chris_ps2_mouse* mouse = kzalloc(sizeof(*mouse), GFP_KERNEL);
    if (!mouse) {
        return -ENOMEM;
    }
    mouse->dev = input_allocate_device();
    serio_set_drvdata(serio, mouse);
    serio_open(serio, drv);
    return 0;
}

static void chris_ps2_disconnect(struct serio* serio) {
    struct chris_ps2_mouse* mouse = serio_get_drvdata(serio);
    serio_close(serio);
    input_free_device(mouse->dev);
    kfree(mouse);
}

static struct serio_driver chris_ps2_driver = {
    .driver = { .name = "chris_ps2_mouse" },
    .interrupt = chris_ps2_interrupt,
    .connect = chris_ps2_connect,
    .disconnect = chris_ps2_disconnect,
};

static int __init chris_ps2_init(void) {
    return serio_register_driver(&chris_ps2_driver);
}

static void __exit chris_ps2_exit(void) {
    serio_unregister_driver(&chris_ps2_driver);
}

module_init(chris_ps2_init);
module_exit(chris_ps2_exit);
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Chris Lab");
