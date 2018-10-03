# flatcrypt

There is a server provided that combines a input message `f` with the flag `PROBLEM_KEY`, then compresses and encrypts it. The relevant code looks like this:

```
if (f>=20):
    data = bytes((PROBLEM_KEY + f).encode('utf-8'))
    ctr = Counter.new(64, prefix=os.urandom(8))
    enc = AES.new(ENCRYPT_KEY, AES.MODE_CTR, counter=ctr).encrypt(zlib.compress(data))
    print("%s%s" %(enc, chr(len(enc))))
```
With the allowed characterset of `f` being lowercase letters and underscore.

What stands out here is that the length of the encrypted message is explicitly returned, and that the data is compressed. Zlib will be more efficient at compressing repetitive data and AES in counter mode does not use padding, so messages already contained in the flag will give a shorter result. We start by repeating a single character 20 times to reach the minimum message size and notice that the letter `o` gives the shortest result. We take this as our partial flag and add another letter, this time giving us `go`, then `ogo` and so on, until the full flag is revealed: `crime_doesnt_have_a_logo`.