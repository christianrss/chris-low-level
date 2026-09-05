// PEDAGOGY-SOLUTION: KMOD-SOURCE-REVIEW-03 — revisão de fonte; não carregado neste ambiente.
#include <linux/module.h>
#include <linux/miscdevice.h>
#include <linux/fs.h>
static int chris_open(struct inode *i, struct file *f){ return 0; }
static int chris_release(struct inode *i, struct file *f){ return 0; }
static const struct file_operations chris_fops={ .owner=THIS_MODULE, .open=chris_open, .release=chris_release };
static struct miscdevice chris_dev={ .minor=MISC_DYNAMIC_MINOR, .name="chris_char", .fops=&chris_fops };
static int __init chris_init(void){ return misc_register(&chris_dev); }
static void __exit chris_exit(void){ misc_deregister(&chris_dev); }
module_init(chris_init); module_exit(chris_exit); MODULE_LICENSE("GPL");
