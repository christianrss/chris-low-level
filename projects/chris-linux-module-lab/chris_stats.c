#include <linux/module.h>
#include <linux/proc_fs.h>
#include <linux/seq_file.h>
#include <linux/atomic.h>
static struct proc_dir_entry *entry; static atomic64_t reads=ATOMIC64_INIT(0);
static int chris_show(struct seq_file *m, void *v){ /* PEDAGOGY-SOLUTION: D8-KMOD-SHOW */ seq_printf(m,"reads=%lld\n",atomic64_inc_return(&reads)); return 0; }
/* PEDAGOGY-SOLUTION: D8-KMOD-OPS */
static int chris_open(struct inode *inode, struct file *file){ return single_open(file,chris_show,NULL); }
static const struct proc_ops chris_ops={.proc_open=chris_open,.proc_read=seq_read,.proc_lseek=seq_lseek,.proc_release=single_release};
static int __init chris_init(void){ /* PEDAGOGY-SOLUTION: D8-KMOD-LIFETIME */ entry=proc_create("chris_stats",0444,NULL,&chris_ops); return entry?0:-ENOMEM; }
static void __exit chris_exit(void){ /* PEDAGOGY-SOLUTION: D8-KMOD-LIFETIME-EXIT */ proc_remove(entry); }
module_init(chris_init); module_exit(chris_exit); MODULE_LICENSE("GPL");
