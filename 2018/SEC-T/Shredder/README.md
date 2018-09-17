# Shredder - Misc

In this challenge, we get floppy.img which is a FAT12 image. We can extract an ELF executable shredder from this image. Then I use testdisk tool to try to recover deleted files and I find flag.txt but it is gibberish or encrypted stuff. If you run the shredder file, you get

> ./shredder passes files

Next step is to reverse the shredder binary to see what it does, and it XORs every byte with the contents of flag.txt file. Therefore, we create this script:

```Python
import sys

with open('flag.txt', 'rb') as f:
    x = f.read()
    for a in range(int(sys.argv[1])):
        tmp = ""
        for i in range(len(x)):
            tmp += chr(ord(x[i]) ^ (0xa1 + a))
        x = tmp
        print(x)

        if "SECT" in x:
            break
```

Then we get the flag: SECT{1f_U_574y_r1gh7_wh3r3_U_R,_7h3n_p30pl3_w1ll_3v3n7u4lly_c0m3_70_U}