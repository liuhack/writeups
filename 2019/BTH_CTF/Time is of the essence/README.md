## Time is of the essence (500 pts) (Programming)

```Crack the password to get the flag. Given a 32-bit x86 ELF binary.```

Running the binary gives us:

```
./time_is_of_the_essence 
Usage: ./time_is_of_the_essence <password>
```

Opening the file in IDA reveals that the binary is compiled using [MoVfuscator](https://github.com/xoreaxeaxeax/movfuscator), which makes it hard to reverse.

<img src="https://i.imgur.com/rnz5HwD.png">

The name of the challenge does however imply a side-channel attack by timing the execution of the program to bruteforce the password. However, our results from timing execution were not consisting so we tried counting the amount of syscalls that were made instead using `strace` which gave us consistent results and gave us the password `pat1enc3_p1eaz3`

```
./time_is_of_the_essence pat1enc3_p1eaz3
Well done! Flag is BTH_CTF{th1s-iz-y0ur-t1M3-t0-shin3-B4By}
```

```python
import string
import sys
from subprocess import PIPE, Popen

result = ''
for i in range(0, 20):
    max_syscalls = 0
    r = ''
    for c in string.printable:
        t = 0
    
        pipe = Popen('strace ./time_is_of_the_essence '+ result + c, shell=True, stdout=PIPE, stderr=PIPE)
        _, stderr = pipe.communicate()
        syscalls = len(stderr.split('\n'))        

        if syscalls > max_syscalls:
            max_syscalls = syscalls
            r = c

    result += r

    sys.stdout.write(r)
    sys.stdout.flush()
```
