## s1mple (422 pts) (Reverse)

```
Can you find the right combination?

given: an x86-64 ELF executable
```

If we run the program, it asks for a password.

```
./simple
What is the password?
asdfasdfasdfa
Wrong!!
```

If we open up the file in radare2 (`r2 -Ad simple`) and disassemble the main function (`pdf@main`), we can see that it make a comparison between your input and some other string. If the two strings are equal, you win!

```
|           0x004006da      bf08084000     mov edi, str.What_is_the_password ; 0x400808 ; "What is the password?" ; const char *s
|           0x004006df      e8ecfdffff     call sym.imp.puts           ; int puts(const char *s)
|           0x004006e4      488d85f0feff.  lea rax, [s1]
|           0x004006eb      4889c7         mov rdi, rax                ; char *s
|           0x004006ee      b800000000     mov eax, 0
|           0x004006f3      e818feffff     call sym.imp.gets           ; char *gets(char *s)
|           0x004006f8      488d95e0feff.  lea rdx, [s2]
|           0x004006ff      488d85f0feff.  lea rax, [s1]
|           0x00400706      4889d6         mov rsi, rdx                ; const char *s2
|           0x00400709      4889c7         mov rdi, rax                ; const char *s1
|           0x0040070c      e8effdffff     call sym.imp.strcmp         ; int strcmp(const char *s1, const char *s2)
|           0x00400711      85c0           test eax, eax
|       ,=< 0x00400713      750c           jne 0x400721
|       |   0x00400715      bf20084000     mov edi, str.flag_is_BTH_CTF_the_password_you_entered_to_reach_this_point ; 0x400820 ; "flag is BTH_CTF{the password you entered to reach this point}" ; const char *s
```

We can see that a pointer to the input string is stored in rax register, and a pointer to the other string is stored in the rdx register.
By setting a breakpoint at the comparison and examining the content at the address stored in rdx, we find the password.

```
[0x7f5504265c30]> db 0x0040070c
[0x7f5504265c30]> dc
What is the password?
adsg
hit breakpoint at: 40070c
[0x0040070c]> ps@rdx
assemblyisfun
```

`BTH_CTF{assemblyisfun}`
