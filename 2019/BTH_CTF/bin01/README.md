```
We intercepted this file in Wireshark. Can you decrypt it? 

Given: a data file named bin01 
```

Examining the file, we see quite a lot of 0x90 bytes.

`hexdump -C bin01`:

```
00000000  ef d5 dc d6 92 91 91 90  90 90 90 90 90 90 90 90  |................|
00000010  93 90 ae 90 91 90 90 90  d0 95 90 90 90 90 90 90  |................|
00000020  d0 90 90 90 90 90 90 90  a0 89 90 90 90 90 90 90  |................|
00000030  90 90 90 90 d0 90 a8 90  99 90 d0 90 8d 90 8c 90  |................|
00000040  96 90 90 90 94 90 90 90  d0 90 90 90 90 90 90 90  |................|
00000050  d0 90 90 90 90 90 90 90  d0 90 90 90 90 90 90 90  |................|
00000060  68 91 90 90 90 90 90 90  68 91 90 90 90 90 90 90  |h.......h.......|
```

This made us suspect that the file had been XOR:ed with 0x90. XOR:ing the file with 0x90 gave us an ELF executable. For some reason it segfaulted when we ran it, but looking at the content with `string` revealed a suspicious-looking string (`QlRIX0NURnsweFhPUi0weEVuY29kZWQtMHhiaW5hcnl9`) which turned out to be the flag encoded in base64.

`BTH_CTF{0xXOR-0xEncoded-0xbinary}`
