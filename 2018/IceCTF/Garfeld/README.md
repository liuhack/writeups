#Garfeld - Crypto

> You found the marketing campaign for a brand new sitcom. Garfeld! It has a secret message engraved on it. Do you think you can figure out what they're trying to say?

We get this image

![garfeld](https://cdn.discordapp.com/attachments/487289459226705943/487311898878935060/unknown.png)

To decrypt this, we first tried https://quipqiup.com/ but it did not give the correct flag. Then we created this script:

```Python
key = [0, 7, 2, 7, 1, 9, 7, 8]
cipher = 'IjgJUOPLOUVAIRUSGYQUTOLTDSKRFBTWNKCFT'

output = ''.join([chr(ord(cipher[x]) - key[x % len(key)]) for x in range(len(cipher))])

print(output)
```

We removed special chars and subtracted the key from each letter. This gives us:

> IceCTFIDONT:HINKGRONSFELDLIKE9MONDA?S

Then the flag is IceCTF{I_DONT_THINK_GRONSFELD_LIKES_MONDAYS}