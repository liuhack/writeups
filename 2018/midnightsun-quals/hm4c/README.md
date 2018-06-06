# Hm4c - crypto
> Some n00b implemented a HMAC, I'm sure you can pwn it.

NOTE: mirror of the blog post at [https://toblu302.github.io/writeup/2018/04/15/midnight-sun-ctf-hm4c-writeup.html](https://toblu302.github.io/writeup/2018/04/15/midnight-sun-ctf-hm4c-writeup.html)

The following post is a writeup for the [Midnight Sun CTF](https://midnightsunctf.se/) online qualifiers. The challenge was to find an encryption key which was used to encrypt some data on a server. You were given some source code of a program, as well as an IP to a server which is running the program.

Connecting to the server gave the following promt:

```
hm4c v1.0 server starting...
Options:
1. Request hmac
2. Quit
```

Pressing 1 and entering some random string gave the following response:

```
Enter data:
asdfoij234098jdofijgdfg
Not valid Base64.
```

So we know that the server software expects something which can be decoded as Base64.

Fortunately, the Python source code running the server was given as a part of the challenge. Here it is, with some of the comments removed for clarity:

```
import sys
import base64
from hashlib import sha256
from flag import FLAG

def to_int(x):
    return int(x.encode("hex"), 16)

def h(x):
    return to_int(
        sha256(str(x)).digest()
    )

def hmac(x):
    val = to_int(x)
    key = to_int(FLAG)
    tmp = key ^ val
    return h(tmp + val)

def _write(msg):
    sys.stdout.write(str(msg) + "\n")
    sys.stdout.flush()

def _read():
    data = sys.stdin.readline().strip()
    return data

_write("hm4c v1.0 server starting...")

while True:
    _write("Options:")
    _write("1. Request hmac")
    _write("2. Quit")

    try:
        choice = int(_read())
    except:
        break

    if choice == 1:
        _write("Enter data:")
        try:
            data = base64.b64decode(_read())
            _write(hmac(data))
        except Exception as e:
            _write("Not valid Base64.")
    elif choice == 2:
        _write("KBye.")
        break
    else:
        _write("Invalid choice.")
        break

_write("Quitting...")
sys.exit()
```

Like we found out earlier, the server tries to parse the input as base64. It then passes the base64-decoded data to the function which calculates the HMAC.
```
data = base64.b64decode(_read())
_write(hmac(data))
```

Let's take a close look at the hmac function.
```
def hmac(x):
    val = to_int(x)
    key = to_int(FLAG)
    tmp = key ^ val
    return h(tmp + val)
```

It parses the base64-decoded input as an integer, and then XORs it with the flag (also parsed as an integer). It then adds the XOR-result to the input and passes it to the function h(x). Taking a close look at the h(x) function, we can see that it essentially takes the SHA256 of the value and parses it as an integer.

```
def h(x):
    return to_int(
        sha256(str(x)).digest()
    )
```

This means that hmac(x) essentially returns SHA256( (key XOR input) + input ), which is what gets printed. Let's use our knowledge of XOR to see if we can find out a way to break this function!

If you take something XOR 0, it's going to return itself (x XOR 0 = x). So if we can get input=0, hmac(input) is going to return SHA256( (key XOR 0) + 0) = SHA256(key). So we need something which gets gets decoded to '0' in base64. Running '_printf "\0" &#124; base64_' informs us that 'AA==' is the string we're after. Sending AA== to the server gives us the following response:

```
26338283963642392056362977586359152896355053870382809550343568157752924630409
```

So we know that SHA256(key) = 26338283963642392056362977586359152896355053870382809550343568157752924630409. Maybe we can use this information to bruteforce the key? Unfortunately, SHA256 takes quite some time to bruteforce. Even though we know some structure of the key, it is still going to take too long. But it is possible to send some clever data the server to retrieve the key. Let's look at _(key XOR input) + input_ again. Suppose that exactly one bit of the input is set. Then when the key gets XORed with the input, that specific bit is going to flip. The following table describes it:

val | 000010000
key | 100101001
key XOR val | 1001**1**1001

After the XOR, the bit gets added in again:

key XOR val | 1001**1**1001
val | 000010000
sum | 101001001

As you can see, sending an input which flipped the fifth bit changed the sum quite a bit, so we no longer compute SHA256( key ). But if we redo the example above, but with the fourth bit set instead of the fifth, we get the following:

val | 000001000
key | 100101001
key XOR val | 10010**1**001

And the addition:

key XOR val | 10010**1**001
val | 000001000
sum | 100101001

The sum ended up being the key again! This is because the XOR flips the set bit of the key to "off", and the addition then adds the bit back in again! We can use this to get the key from the server, one bit at a time. If we send in 1 and get back the same number as we did for 0, we know that the first bit of the key is set. If we get back a different number, we know that the first bit of the key is not set. You can then proceed to send in 2 (binary 10), 4 (binary 100), 8 (binary 1000) and so on.

When I found this out, I generated 256 different Base64-encoded strings of integers with exactly one digit set. Then I made a python-script which reads the strings, sends them to the server, and prints out a 1 or a 0, depending on if the previous number was returned.

```
import os
import socket
import sys
import time

def netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    retval = []
    while True:
        data = s.recv(4096)
        if not data:
            break
        retval.append( repr(data) )
    s.close()
    return retval

for line in sys.stdin:
  data = line.strip()
  resp = netcat( [SERVER IP], 31337, "1\n" + data + " \n2" )
  time.sleep(0.1)
  if( "26338283963642392056362977586359152896355053870382809550343568157752924630409" in resp[1] ):
    print( "1" )
  else:
    print( "0" )
```

The netcat function was take from [Stack Overflow](https://stackoverflow.com/questions/1908878/netcat-implementation-in-python) and modified slightly to do what I want. I ran the script with '_python < base64_strings.txt_'.

After some time, the script printed out the following sequence:

1011111011000010001011001011001000010010111110100010001000001100111101101110001011111010100000101111101000101110000011000111001011111010110010101000110011111010001001001000110000010110001010101101111000101110000101101110011010010110011101100010011010010110

Reversing the digits and putting it trough some online [binary to string converter](https://codebeautify.org/binary-string-converter) revealed the flag:

```
idnight{Th1$_1S_N0t_A_Go0D_HM4C}
```

Or well, most of it. The part inside {} is all that's needed, so only getting 256 bits was quite enough.

Lessons learned from this challenge: Even if you use something hard-to-crack like SHA256, you can still end up with something broken if you do some mathematically unsound pre-calculation!

