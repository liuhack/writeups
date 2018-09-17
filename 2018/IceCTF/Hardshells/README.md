#Hard shells - Forensics

> After a recent hack, a laptop was seized and subsequently analyzed. The victim of the hack? An innocent mexican restaurant. During the investigation they found this suspicous file. Can you find any evidence that the owner of this laptop is the culprit?

We first get a password protected zip file, so we use fcrackzip to crack the password and the password is tacos. Then we get a filesystem

> hardshells: Minix filesystem, V1, 30 char names, 20 zones

Next step is to mount the filesystem. Then we look through the files and we got some contents in .bash_history, especially 

> ./tool.py ../secret > ../hzpxbsklqvboyou 

The file hzpxbsklqvboyou contains this encrypted information:
> 8NHY25mYthGfs5ndwx2Zk1lcaFGc4pWdVZFQoJmT8NHY25mYthGfs5ndwx2Zk1lcaFGc4pWdVZFQoJmT8NHY25mYthGfs5ndwx2Zk1lcaFGc4pWdVZFQoJmT8NHY25mYthGfs5ndwx2Zk1lcaFGc4pWdVZFQoJmT8NHY25mYthGfs5ndwx2Zk1lcaFGc4pWdVZFQoJmT

Then we find tool.py which contains this script:

```Python
#!/usr/bin/python3
import sys
import base64

def encode(filename):
    with open(filename, "r") as f:
        s = f.readline().strip()
        return base64.b64encode((''.join([chr(ord(s[x])+([5,-1,3,-3,2,15,-6,3,9,1,-3,-5,3,-15] * 3)[x]) for x in range(len(s))])).encode('utf-8')).decode('utf-8')[::-1]*5

if __name__ == "__main__":
    print(encode(sys.argv[1]))
```

Right now, we have tool.py and the encrypted file name but not the input secret which the author ran as argument to the tool.py file. This means we have to reverse the script. The easiest way to do that is to write a new script which does the same things as tool.py but in reversed order. 

```Python
import base64

input = '8NHY25mYthGfs5ndwx2Zk1lcaFGc4pWdVZFQoJmT'

input = input[::-1]

input = input.encode('utf-8')

input = base64.b64decode(input)

input = input.decode('utf-8')

key = [5,-1,3,-3,2,15,-6,3,9,1,-3,-5,3,-15] * 3

output = ''.join([chr(ord(input[x]) - key[x]) for x in range(len(input))])

print(output)
```

This gives us the flag: IceCTF{good_ol_history_lesson}