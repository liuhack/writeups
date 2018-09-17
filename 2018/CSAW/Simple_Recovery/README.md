#Simple recovery - Forensics

We are given two RAID5 disk images and the first we tried was to recover these using OSForensics and then mount it but that gave us that it was corrupted. Then we just tried a simple grep for flag on one of the images:

> strings disk.img0 | grep flag

This gave us the flag directly: flag{dis_week_evry_week_dnt_be_securty_weak}