#Rewind- Forensics

We are given a zip file which contains two files: rewind-rr-snp and rewind-rr-nodent.log. If we do file command on the first one, we get

> QEMU suspend to disk image

Then first thing I try is to grep for flag

> strings rewind-rr-snp | grep flag{

Then we found the flag{RUN_R3C0RD_ANA1YZ3_R3P3AT} in the result.
