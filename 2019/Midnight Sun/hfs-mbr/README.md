# hfs-mbr

```
 We made a military-grade secure OS for HFS members. Feel free to beta test it for us!

    settings Service: stty -icanon -echo ; nc hfs-os-01.play.midnightsunctf.se 31337 ; stty sane 

    cloud_download Download: hfs-os.tar.gz https://s3.eu-north-1.amazonaws.com/dl.2019.midnightsunctf.se/529C928A6B855DC07AEEE66037E5452E255684E06230BB7C06690DA3D6279E4C/hfs-os.tar.gz
```

For this challenge, we were given a disk image with instruction on how to boot it in QEMU. We were asked for a password when we started it, so it was clear that the goal was to obtain the correct password.

An included README had instructions on how to attach IDA, and where to set a breakpoint.

```
./run debug (gdb stub) or ./run

How to debug with IDA
In IDA > Debugger > Attach > Remote debugger (host:1234) > (Debug options > Set specific options, UNCHECK 'software breakpoints at eip+1', CHECK 'use CS:IP in real mode')  > OK  
When attached, Debugger > Manual memory regions > Insert > CHECK 16bit segment > OK  
In the IDA-View, press G, 0x7c00 is where the bootloader starts. Set a BP > F9
```

We used radare2 instead of IDA, but the same idea applies.

`r2 -D gdb gdb://localhost:1234 -b 16`
`db 0x7c00`
`dc`

From here we stepped one syscall at a time (with `dcs`) until we reached the point where the first character of the password is read, at address 0x7e3b. Looking at the disassembly at the code from that position, we could figure out the following:

* One character is read at a time.
* This character determines where we jump next. Every character except for e,j,n,o,p,r,s,u and w jump to some dead code.
* If you jump to the code of any of the above characters, a check is made which increases a counter if successful.
* If this counter reaches 9, you win!

Here is the disassembly of the code you jump to when you hit 'e'. dl stores the current character (0x65 for 'e'), and at [0x81ba] we find the number of characters read so far. The goal is to jump to 0x7fce.
```
0000:7e86      b8adde         mov ax, 0xdead
0000:7e89      3216ba81       xor dl, byte [0x81ba]
0000:7e8d      31c0           xor ax, ax
0000:7e8f      0410           add al, 0x10
0000:7e91      0410           add al, 0x10
0000:7e93      0410           add al, 0x10
0000:7e95      0410           add al, 0x10
0000:7e97      0410           add al, 0x10
0000:7e99      0410           add al, 0x10
0000:7e9b      28c2           sub dl, al
0000:7e9d      80fa02         cmp dl, 2
0000:7ea0      0f853501       jne 0x7fd9
0000:7ea4      e92701         jmp 0x7fce
```
We can see that the requirement is that `('e' XOR CharactersRead) - 0x60` should equal `2`. This means that 'e' should go in position 7 of the password.

Similar requirements could be found for the other characters. In the end, the password `sojupwner` was obtained. Sending it to the server gave us the flag.

`midnight{w0ah_Sh!t_jU5t_g0t_REALmode}`